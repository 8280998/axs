# axs
Axie Infinity：Atia's Legacy 预注册活动，邮箱注册脚本

## 运行环境

1.Python 3.x：确保系统已安装 Python 3.x。

    sudo apt update

    sudo apt install -y libnss3 libatk-bridge2.0-0 libcups2 libxcomposite1 libxrandr2 libxdamage1 libgbm-dev libxshmfence-dev fonts-liberation

    sudo apt install python3 python3-pip

2. 安装 Playwright

    pip3 install playwright

    playwright install

    playwright install-deps

4. 安装其他 Python 依赖

   pip3 install requests imaplib2
   
5. 配置邮箱访问
   
Gmail 应用专用密码：

访问 Google 账号设置。

进入 安全性 > 应用密码，生成一个新的应用密码。

7. 准备 test.txt 文件
   
test.txt 文件：在代码运行的目录下创建一个 test.txt 文件，内容格式为：

邮箱名|专用密码 example@gmail.com|your_app_password

9. 运行代码
    
运行脚本：确保你在代码所在的目录下，然后运行以下命令：

  python3 axs_register.py
