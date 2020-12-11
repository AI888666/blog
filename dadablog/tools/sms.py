import base64
import datetime
import hashlib
import json
from django.conf import settings
import requests


class YunTongXin():
    base_url = "https://app.cloopen.com:8883"

    def __init__(self, accountSid, accountToken, appId, templateId):
        self.accountSid = accountSid  # 账户ID
        self.accountToken = accountToken  # 授权令牌
        self.appId = appId
        self.templateId = templateId

    def get_request_url(self, sig):
        """
            生成具体通信的url
        :param sig: 校验签名
        :return:
        """
        # /2013-12-26/Accounts/{accountSid}/SMS/{funcdes}?sig={SigParameter}
        self.url = self.base_url + '/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s' % (self.accountSid, sig)
        return self.url

    # 签名：账户Id + 账户授权令牌 + 时间戳
    def get_sig(self, timestamp):
        """
            生成签名
        :param timestamp: 时间戳
        :return:
        """
        s = self.accountSid + self.accountToken + timestamp
        m = hashlib.md5()
        m.update(s.encode())
        return m.hexdigest().upper()

    def get_timesatmp(self):
        """
            生成时间戳
        :return:
        """
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    def get_request_header(self, timestamp):
        """
            生成请求头
        :param timestamp: 时间戳
        :return:
        """
        s = self.accountSid + ":" + timestamp
        auth = base64.b64encode(s.encode()).decode()
        return {
            "Accept": "application/json",
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": auth
        }

    def get_request_body(self, phone, code):
        """
            请求体
        :param phone: 手机号
        :param code: 验证码
        :return:
        """
        return {
            "to": phone,
            "appId": self.appId,
            "templateId": self.templateId,
            "datas": [code, "1"]
        }

    def request_api(self, url, header, body):
        """
            发送请求
        :param url:
        :param header:
        :param body:
        :return:
        """
        res = requests.post(url, headers=header, data=body)
        return res.text

    def run(self, phone, code):
        # 获取时间戳
        timestamp = self.get_timesatmp()
        # 生成签名
        sig = self.get_sig(timestamp)
        # 生成　业务 url
        url = self.get_request_url(sig)
        # print(url)
        # 请求头
        header = self.get_request_header(timestamp)
        # print(header)
        # 请求体
        body = self.get_request_body(phone, code)
        # 请求发送
        data = self.request_api(url, header, json.dumps(body))
        return data


# 测试
if __name__ == "__main__":
    config = {
        "accountSid": "8aaf070875da65fe0175db622dbd0075",
        "accountToken": "15c26146555946b49ff77b342f2d1289",
        "appId": "8aaf070875da65fe0175db622ed0007b",
        "templateId": "1"
    }
    print(settings.ACCOUNT_SID)
    yun = YunTongXin(**config)
    res = yun.run("18798345496", "921210")
    print(res)

# 【云通讯】　您使用的是云通信短信模板，您的验证码是９２１２１０，请于２分钟内正确输入
