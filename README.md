# axs
Axie Infinity：Atia's Legacy 预注册活动，邮箱注册脚本

Python 环境
Python 3.x：确保系统已安装 Python 3.x。你可以通过以下命令检查 Python 版本：
python3 --version
如果没有安装，可以使用以下命令安装：

sudo apt update
sudo apt install python3 python3-pip
2. 安装 Playwright
Playwright：这是一个用于自动化浏览器操作的库。你可以通过以下命令安装：
Copy
pip3 install playwright
安装完成后，需要安装 Playwright 的浏览器驱动：
Copy
playwright install
3. 安装其他 Python 依赖
其他依赖：虽然代码中没有明确提到其他依赖，但建议安装以下常用库（如果还没有安装）：
Copy
pip3 install requests imaplib2
4. 安装浏览器
Chromium：Playwright 默认使用 Chromium 浏览器。你可以通过以下命令安装 Chromium：
Copy
sudo apt install chromium-browser
如果你想使用其他浏览器（如 Firefox 或 WebKit），也可以通过 Playwright 安装对应的浏览器驱动。
5. 配置邮箱访问
Gmail 应用专用密码：如果你使用 Gmail 获取验证码，需要为你的 Gmail 账号生成一个应用专用密码（App Password），因为 Gmail 默认禁用了少安全应用的访问。
访问 Google 账号设置。
进入 安全性 > 应用密码，生成一个新的应用密码。
将应用密码替换代码中的 email_password。
6. 准备 test.txt 文件
test.txt 文件：在代码运行的目录下创建一个 test.txt 文件，内容格式为：
Copy
邮箱名|专用密码
例如：
Copy
example@gmail.com|your_app_password
7. 运行代码
运行脚本：确保你在代码所在的目录下，然后运行以下命令：
