import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# QQ邮箱账户以及密码
QQ_ACCOUNT = "*******@qq.com"
QQ_PASSWORD = "**********"

# 网易账户以及密码
WANG163_ACCOUNT = "********@163.com"
WANG163_PASSWORD = "151********guan"

class AutoEmail:

    def login_info(self, user, passwd):
        """
        设置登陆信息
        需要参数有：账户，密码
        :param user:
        :param passwd:
        :return:
        """
        self.user = user
        self.passwd = passwd

    def send_info(self, receiver, sender=None):
        """
        设置发送信息
        需要参数：接受者，发送者
        :param receiver:
        :param sender:
        :return:
        """
        # 如果账户就是发送邮箱，那么可以不填
        if not sender:
            self.sender = self.user
        else:
            self.sender = sender

        self.receiver = receiver

    def create_letter(self, title, content):
        """
        构建邮件
        需要参数：邮件主题，邮件内容
        最后返回“一封信”
        :param title:
        :param content:
        :return:
        """
        msg = MIMEMultipart()
        msg.attach(MIMEText(content, "plain", "utf-8"))
        msg["subject"] = title
        msg["from"] = self.sender
        msg["to"] = self.receiver

        return msg

    def file_attachment(self, filePath):
        """
        添加文件附件
        需要参数：文件路径
        最后返回”附件“
        :param filePath:
        :return:
        """
        attachment = MIMEText(open(filePath, "rb").read(), "base64", "utf-8")
        # attachment = MIMEText("hello,world", "plain", "utf-8")
        attachment["Content-Type"] = "application/octet-stream"

        # 利用正则，获取文件名字，以及文件格式
        createName = re.search(r"(.+?)(\..+)", filePath.split("\\")[-1])
        fileName = createName.group(1)
        fileFormat = createName.group(2)
        attachment["Content-Disposition"] = 'attachment; filename='+fileName+fileFormat
        # attachment["Content-Disposition"] = "attachment; filename=1.txt"

        return attachment

    def execute(self, msg, attachments=[]):
        """
        仅起提示作用
        :param args:
        :param kwargs:
        :return:
        """
        # self.__class__.__name__当前类的名字
        serverHost, smtpMethod = self.choose_server(self.__class__.__name__)
        # 返回字符串，eval()方法将其还原并执行
        smtp = eval(smtpMethod)()

        # 如果存在附件，遍历附件，加入邮件当中
        if attachments:
            for item in attachments:
                msg.attach(item)

        try:
            # 连接邮箱服务器，并且登陆
            smtp.connect(serverHost)
            smtp.login(self.user,self.passwd)
        except Exception as e:
            # 如果失败，打印原因，并且退出程序
            print("【FAILURE】There is the reason as follows:")
            print(e)
            return

        try:
            # 发送邮件
            smtp.sendmail(self.sender, self.receiver, msg.as_string())
        except smtplib.SMTPDataError as e:
            # 如果失败，打印原因
            print("MISTAKE")
            print(e)
            return
        finally:
            # 无论邮件发送成功与否都退出连接
            smtp.quit()

        # 如果成功，输出提示
        print("【SUCCESS】")

    def choose_server(self, className):
        """
        选择服务商以及创建smpt对象方式
        :param className:
        :return:
        """
        option = {
            "Email163": ("smtp.163.com", "smtplib.SMTP"),
            "EmailQQ": ("smtp.qq.com", "smtplib.SMTP_SSL")
        }

        return option[className]


class Email163(AutoEmail):
    """
    利用网易163邮箱发送邮件
    """
    def __init__(self):
        super().__init__()


class EmailQQ(AutoEmail):
    """
    利用QQ邮箱发送邮件
    """
    def __init__(self):
        super().__init__()
