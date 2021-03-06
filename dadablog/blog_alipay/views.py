# import json
# import time
# from .models import Money
# from django.http import JsonResponse
# from django.shortcuts import render
# from django.views import View
# from django.conf import settings
# from alipay import AliPay
# from topic.models import Topic
#
# app_private_key_string = open(settings.ALIPAY_KEY_DIRS + 'app_private_key.pem').read()
# alipay_public_key_string = open(settings.ALIPAY_KEY_DIRS + 'app_public_key.pem').read()
#
#
# class MyAliPay(View):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.alipay = AliPay(
#             appid=settings.ALIPAY_ID,
#             app_private_key_string=app_private_key_string,
#             alipay_public_key_string=alipay_public_key_string,
#             app_notify_url=None,
#             sign_type='RSA2',
#             debug=True,
#         )
#
#     # 支付绑定地址 -- 订单ｉｄ，订单价格
#     def get_trade_url(self, order_id, amount):
#         order_string = self.alipay.api_alipay_trade_page_pay(
#             subject=order_id,
#             out_trade_no=order_id,
#             total_amount=amount,
#             return_url=settings.ALIPAY_RETURN_URL,
#             notify_url=settings.ALIPAY_NOTIFY_URL,
#         )
#         return 'https://openapi.alipaydev.com/gateway.do?' + order_string
#
#
# class OrderView(MyAliPay):
#
#     def post(self, request):
#         # 获取数据
#         json_str = request.body
#         json_obj = json.loads(json_str)
#         order_id = json_obj['topic_id']
#         money = json_obj['money']
#         user = json_obj['title']
#         topic = Topic.objects.filter(author=user).first()
#         # print('===')
#         # print(topic)
#         # print('===')
#         # order_id = '%sxHH' % time.time()
#         pay_url = self.get_trade_url(order_id, money)
#         Money.objects.create(money=money, order_id=order_id, topic=topic)
#
#         return JsonResponse({'pay_url': pay_url})
import json
import time

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
from alipay import AliPay
from tools.logging_dec import logging_check

app_private_key_string = open(settings.ALIPAY_KEY_DIRS + 'app_private_key.pem').read()
alipay_public_key_string = open(settings.ALIPAY_KEY_DIRS + 'app_public_key.pem').read()


class MyAliPay(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alipay = AliPay(
            appid=settings.ALIPAY_ID,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            app_notify_url=None,
            sign_type='RSA2',
            debug=True,  # 默认是Ｆalse　True则是将请求转发沙箱环境
        )

    # 支付绑定地址 -- 订单ｉｄ，订单价格
    def get_trade_url(self, order_id, amount):
        order_string = self.alipay.api_alipay_trade_page_pay(
            subject=order_id,
            out_trade_no=order_id,
            total_amount=amount,
            # 支付完毕，将用户跳转至哪个页面
            return_url='http://127.0.0.1:5000/',
            notify_url='http://127.0.0.1:5000/',
        )
        return 'https://openapi.alipaydev.com/gateway.do?' + order_string

    def get_verify_result(self, data, sign):
        # 验证签名　True 成功　False　失败
        return self.alipay.verify(data, sign)

    def get_trade_result(self, order_id):
        # 主动查询
        result = self.alipay.api_alipay_trade_query(order_id)
        if result.get('trade_status') == 'TRADE_SUCCESS':
            return True
        return False


class OrderView(MyAliPay):

    # def get(self, request):
    #     return render(request, 'alipay.html')
    def post(self, request):
        # 获取数据
        json_str = request.body
        json_obj = json.loads(json_str)
        order_id = json_obj['topic_id']
        money = json_obj['money']
        username = json_obj['username']
        print(username)
        print('=='*8)
        print(money)
        # order_id = '%sxHH' % time.time()
        pay_url = self.get_trade_url(order_id, money) + username + '/topics'
        # pay_url = 'http://127.0.0.1:5000/' + username + '/topics'
        print(pay_url)
        return JsonResponse({'pay_url': pay_url})


class ResultView(MyAliPay):
    def post(self, request):
        # notify_url 业务逻辑
        request_data = {k: request.POST[k] for k in request.POST.keys()}
        sign = request_data.pop('sign')
        is_verify = self.get_verify_result(request_data, sign)
        if is_verify is True:
            # 当前请求是支付宝发的
            trade_status = request_data.get('trade_status')
            if trade_status == 'TRADE_SUCCESS':
                print('-------------支付成功！')
                # 修改自己的数据库里的订单状态，例如　代付款　已付款
                return JsonResponse('success')
        else:
            return HttpResponse('违法请求！')

    def get(self, request):
        # ｒreturn_url 业务逻辑
        order_id = request.GET['out_trade_no']
        # 查询订单表状态，如果还是代付款，采取Ｂ方案－主动查询支付宝　订单真实交易状态
        # 主动查询
        result = self.get_trade_result(order_id)
        if result:
            return HttpResponse('--支付成功--主动查询')
        else:
            return HttpResponse('--支付异常--主动查询')