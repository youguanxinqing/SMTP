"""
演示代码
"""
from autoEmail import *


def main():

    qqemail = EmailQQ()
    qqemail.login_info(QQ_ACCOUNT, QQ_PASSWORD)
    qqemail.send_info(WANG163_ACCOUNT)

    title = "端午节快乐"
    content = "大家好哇？粽子节快乐！"
    msg = qqemail.create_letter(title, content)
    att = qqemail.file_attachment("de.jpeg")
    qqemail.execute(msg, [att])

if __name__ == "__main__":
    main()