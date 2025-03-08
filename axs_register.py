import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import random
import string
import time
import re
import imaplib
import email
from email.header import decode_header
from datetime import datetime
import sys
import os

sys.stdout = open(sys.stdout.fileno(), 'w', buffering=1)


def get_verification_code(email_address, email_password, keyword="Axie Infinity", max_checks=5, timeout=300):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        mail.login(email_address, email_password)
        mail.select("inbox")

        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 初始等待 10 秒，确保邮件同步...")
        time.sleep(10)
        check_start_time = time.time()
        wait_interval = 5
        check_count = 0
        while time.time() - check_start_time < timeout and check_count < max_checks:
            mail.select("inbox")
            mail.noop()

            status, data = mail.search(None, f'(TEXT "{keyword}")')
            if not data[0]:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 未找到包含 '{keyword}' 的邮件，等待 {wait_interval} 秒后重试... (检查 {check_count + 1}/{max_checks})")
                time.sleep(wait_interval)
                wait_interval = min(wait_interval + 5, 20)
                check_count += 1
                if check_count >= max_checks:
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 达到最大检查次数 {max_checks}，跳过当前用户")
                    return None
                continue

            email_ids = data[0].split()
            if not email_ids:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 邮件列表为空，等待 5 秒后重试...")
                time.sleep(5)
                continue

            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 找到 {len(email_ids)} 封包含 '{keyword}' 的邮件，检查最新 5 封...")

            email_ids = email_ids[-5:]

            for email_id in reversed(email_ids):
                status, data = mail.fetch(email_id, "(RFC822)")
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)

                subject = decode_email_subject(msg["subject"])
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 检查邮件，主题: {subject}, 邮件 ID: {email_id}")

                from_header = msg.get("From", "").lower()
                if "axieinfinity.com" in from_header and "legacy verification" in subject.lower():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain" or content_type == "text/html":
                            body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                            code_match = re.search(r"\b\d{6}\b", body) or re.search(r"\d{6}", body)
                            if code_match:
                                code = code_match.group(0)
                                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 找到验证码: {code}，从主题 {subject} 的正文中提取")
                                mail.store(email_id, '+FLAGS', '\\Seen')
                                return code

                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 邮件不匹配或未找到验证码")

            time.sleep(wait_interval)

        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 超时 {timeout} 秒或达到最大检查次数，未找到匹配的未读邮件或验证码")
        return None

    except imaplib.IMAP4.error as e:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IMAP 错误: {e}")
        return None
    except Exception as e:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 发生错误: {e}")
        return None
    finally:
        try:
            mail.logout()
        except:
            pass

def decode_email_subject(subject):
    decoded_subject = decode_header(subject)[0][0]
    if isinstance(decoded_subject, bytes):
        try:
            return decoded_subject.decode()
        except:
            return decoded_subject.decode("utf-8", errors="ignore")
    return decoded_subject

async def register_user(page, email_address, email_password, user_index):
    start_time = time.time()
    max_retries = 3
    for attempt in range(max_retries):
        # 设置你的大号邀请连接,ref=xxxxxx修改为你的邀请码
        try:
            await page.goto("https://axieinfinity.com/pre-register/?ref=xxxxxx", wait_until="networkidle", timeout=60000)
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：访问注册页面")
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(5000) 
            break
        except PlaywrightTimeoutError:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：页面加载超时，第 {attempt + 1}/{max_retries} 次尝试")
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(5)

    # 设置转发邮箱域名，将example.com修改为你的转发域名。当前代码只支持gmail邮箱接收
    try:
        letters = ''.join(random.choices(string.ascii_lowercase, k=8))
        email = f"{letters}@example.com"
        await page.fill("input[placeholder='Enter your email']", email)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：生成并输入邮箱: {email}")
    except PlaywrightTimeoutError:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：未找到邮箱输入框，请确认选择器")
        return

    try:
        await page.wait_for_selector("button:has-text('Pre-Register')", state="visible", timeout=10000)
        await page.click("button:has-text('Pre-Register')")
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：点击 Pre-Register")
        await page.wait_for_timeout(10000)
    except PlaywrightTimeoutError:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：未找到 Pre-Register 按钮，请确认页面状态")
        html = await page.content()
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：页面 HTML 片段（前 2000 字符）：{html[:2000]}")
        return

    try:
        await page.wait_for_selector(".dango-dialog-body", state="visible", timeout=15000)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：对话框已加载")
    except PlaywrightTimeoutError:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：未找到对话框（.dango-dialog-body），请确认页面状态")
        return

    code = get_verification_code(email_address, email_password)
    if code:
        try:
            await page.wait_for_selector(".input-module_form__2zFJF input[placeholder='Input verification code']", state="visible", timeout=10000)
            await page.fill(".input-module_form__2zFJF input[placeholder='Input verification code']", code)
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：填写验证码: {code}")
        except PlaywrightTimeoutError:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：未找到验证码输入框，请确认选择器")
            return

        try:
            await page.wait_for_selector("button.custom-button_container__1Ruz3:has-text('Confirm')", state="visible", timeout=15000)
            await page.click("button.custom-button_container__1Ruz3:has-text('Confirm')")
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：点击 Confirm")
            await page.wait_for_timeout(2000)
        except PlaywrightTimeoutError:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：未找到 Confirm 按钮，请确认页面状态")
            html = await page.content()
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：页面 HTML 片段（前 2000 字符）：{html[:2000]}")
            return

        success = await handle_image_verification(page)
        if success:
            with open("address.txt", "a") as f:
                f.write(f"{email}\n")
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：保存到 address.txt: {email}")

            delay = random.randint(1, 5)
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：等待 {delay} 秒后关闭浏览器并注册下一个用户")
            await asyncio.sleep(delay)
        else:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：图片验证失败，跳过此用户")
    else:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index}：验证码获取失败，跳过此用户")

    end_time = time.time() 
    elapsed_time = end_time - start_time 
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {user_index} 会话已清理，耗时 {elapsed_time:.2f} 秒")

async def handle_image_verification(page):
    start_time = time.time()
    timeout = 180

    while time.time() - start_time < timeout:
        try:
            await page.wait_for_selector("button.axie-captcha-confirm-button", state="visible", timeout=15000)
            await page.click("button.axie-captcha-confirm-button")
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 点击图片验证 Confirm")
            await page.wait_for_timeout(2000)

            if await page.is_visible("button.custom-button_container__1Ruz3:has-text('Confirm')"):
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 图片验证失败，返回到填写验证码的窗口")
                await page.click("button.custom-button_container__1Ruz3:has-text('Confirm')")
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 再次点击填写验证码的 Confirm 按钮")
                await page.wait_for_timeout(2000)
            else:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 图片验证成功")
                return True

        except (PlaywrightTimeoutError, Exception) as e:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 图片验证确认按钮未找到或请求失败: {e}")
            return False

        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 图片验证失败，重试...")
        await page.wait_for_timeout(2000)

    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 图片验证超时，跳过当前用户")
    return False

async def main():
    start_time = datetime.now()
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 脚本启动时间: {start_time}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)


        users = []
        try:
            with open("test.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if line and "|" in line:
                        email_address, email_password = line.split("|", 1)
                        users.append((email_address.strip(), email_password.strip()))
            if not users:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} test.txt 为空或格式错误，请检查文件内容")
                return
        except FileNotFoundError:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} test.txt 文件未找到，请创建文件并添加格式为 '邮箱名|专用密码' 的内容")
            return
        except Exception as e:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 读取 test.txt 失败: {e}")
            return

        # 自定义注册数量，默认100个。短时间内过多请求会出现429状态码，具体时间数据没测试出来
        TOTAL_USERS = 100
        users = users * (TOTAL_USERS // len(users)) + users[:TOTAL_USERS % len(users)]

        for i in range(TOTAL_USERS):
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 开始注册用户 {i+1}/{TOTAL_USERS}")
            context = await browser.new_context()
            page = await context.new_page()

            try:
                await register_user(page, users[i % len(users)][0], users[i % len(users)][1], i + 1)
            except Exception as e:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 用户 {i+1} 注册失败: {e}")
            finally:
                await context.close()

            await asyncio.sleep(random.randint(15, 30))

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
