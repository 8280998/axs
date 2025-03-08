# axs自动注册邮箱
———————————————————————————————————————————————

Axie Infinity：Atia's Legacy 预注册活动，邮箱自动注册脚本

准备一个域名，在forwardemail或其他类似网站登记这个域名转发功能，转发到你的GMAIL邮箱

———————————————————————————————————————————————

## 运行环境

1.Python 3.x：确保系统已安装 Python 3.x。

    sudo apt update

    sudo apt install -y libnss3 libatk-bridge2.0-0 libcups2 libxcomposite1 libxrandr2 libxdamage1 libgbm-dev libxshmfence-dev fonts-liberation

    sudo apt install python3 python3-pip

2. 安装 Playwright

        pip3 install playwright

        playwright install

        playwright install-deps

3. 安装其他 Python 依赖

        pip3 install requests imaplib2
   
4. 配置邮箱访问
   
Gmail 应用专用密码：

访问 Google 账号设置。

进入 安全性 > 应用密码，生成一个新的应用密码。


5. 准备 test.txt 文件
   
test.txt 文件：在代码运行的目录下创建一个 test.txt 文件，内容格式为：

邮箱名|专用密码

6.修改配置

第一个修改注册的数量，第二个是注册的转发域名，第三个是你的大号邀请连接
——————————————————————————————————————————————————————————

        # 自定义注册数量，默认1000个。可在此处自定义注册数量
        TOTAL_USERS = 1000
——————————————————————————————————————————————————————————

            # 设置转发邮箱域名，将example.com修改为你的转发域名。当前代码只支持gmail邮箱接收
    try:
        letters = ''.join(random.choices(string.ascii_lowercase, k=8))
        email = f"{letters}@example.com"
——————————————————————————————————————————————————————————

        # 设置你的大号邀请连接,ref=xxxxxx修改为你的邀请码
        try:
            await page.goto("https://axieinfinity.com/pre-register/?ref=xxxxxx", wait_until="networkidle", timeout=60000)

——————————————————————————————————————————————————————————

7. 运行代码
 
        python3 axs_register.py

8.运行界面如下
![image](https://github.com/user-attachments/assets/887e42ba-ed01-44a3-9245-11ea288540c0)


