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

4. 安装其他 Python 依赖

        pip3 install requests imaplib2
   
   
5. 配置邮箱访问
   
Gmail 应用专用密码：

访问 Google 账号设置。

进入 安全性 > 应用密码，生成一个新的应用密码。


6. 准备 test.txt 文件
   
test.txt 文件：在代码运行的目录下创建一个 test.txt 文件，内容格式为：

邮箱名|专用密码

7.修改配置

第一个地方是修改需要注册的数量，第二个是注册的域名
——————————————————————————————————————————————————————————

        # 自定义注册数量，默认1000个。可在此处自定义注册数量
        TOTAL_USERS = 1000
——————————————————————————————————————————————————————————

            # 设置转发邮箱域名，将example.com修改为你的转发域名。当前代码只支持gmail邮箱接收
    try:
        letters = ''.join(random.choices(string.ascii_lowercase, k=8))
        email = f"{letters}@example.com"
——————————————————————————————————————————————————————————

9. 运行代码
 
        python3 axs_register.py

10.运行界面如下
![image](https://github.com/user-attachments/assets/51e8df5f-83f6-47f0-a268-b7df5ef114d7)

