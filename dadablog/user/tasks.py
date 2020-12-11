from dadablog.celery import app
from tools.sms import YunTongXin


@app.task
def send_sms_c(phone, code):
    """
        发送短息
    :param phone: 手机号
    :param code: 随机码
    :return:
    """
    config = {
        "accountSid": "8aaf070875da65fe0175db622dbd0075",
        "accountToken": "15c26146555946b49ff77b342f2d1289",
        "appId": "8aaf070875da65fe0175db622ed0007b",
        "templateId": "1"
    }
    yun = YunTongXin(**config)
    res = yun.run(phone, code)
    return res
