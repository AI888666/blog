import base64
import datetime
import hashlib
import json

import requests  # 用来发请求http/https请求


class YunTongXin():
    base_url = 'https://app.cloopen.com:8883'

    def __init__(self, accountSid, accountToken, appId, templateId):
        self.accountSid = accountSid  # 账号id
        self.accountToken = accountToken  # 授权令牌
        self.appId = appId  # 应用id
        self.templateId = templateId  # 模板id

    def get_requset_url(self, sig):
        """
            生成具体通信的url
        :param sig: 校验签名
        :return:
        """
        # /2013-12-26/Accounts/{accountSid}/SMS/{funcdes}?sig
        # = {SigParameter}
        self.url = self.base_url + '/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s' % (self.accountSid, sig)
        return self.url

    # 账户Id + 账户授权令牌 + 时间戳
    def get_sig(self, timestamp):
        """
            生成签名
        :param timestamp:时间戳
        :return:
        """
        s = self.accountSid + self.accountToken + timestamp
        m = hashlib.md5()
        m.update(s.encode())
        return m.hexdigest().upper()

    def get_timestamp(self):
        """
            生成时间戳
        :return:
        """
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def get_request_header(self, timestamp):
        """
            生成请求头
        :param timestamp: 时间戳
        :return:
        """
        s = self.accountSid + ':' + timestamp
        auth = base64.b64encode(s.encode()).decode()
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': auth
        }

    def get_request_body(self, phone, code):
        """
            请求体
        :param phone: 手机号
        :param code: 验证码
        :return:
        """
        return {
            'to': phone,
            'appId': self.appId,
            'templateId': self.templateId,
            'datas': [code, '3']
        }

    def request_api(self, url, header, body):
        res = requests.post(url, headers=header, data=body)
        return res.text

    def run(self, phone, code):
        # 获取时间戳
        timestamp = self.get_timestamp()
        # 生成签名
        sig = self.get_sig(timestamp)
        # 生成业务 url
        url = self.get_requset_url(sig)
        # print(url)
        header = self.get_request_header(timestamp)
        # print(header)
        # 生成请求体
        body = self.get_request_body(phone, code)
        # print(body)
        # 发请求
        data = self.request_api(url, header, json.dumps(body))
        return data


if __name__ == "__main__":
    config = {
        "accountSid": "8aaf070875da65fe0175db622dbd0075",
        "accountToken": "15c26146555946b49ff77b342f2d1289",
        "appId": "8aaf070875da65fe0175db622ed0007b",
        "templateId": "1"
    }

    yun = YunTongXin(**config)
    res = yun.run("18798345496", "888666")
    print(res)
