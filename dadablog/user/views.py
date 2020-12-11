import json
import random
import re
import hashlib
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from .models import UserProfile
from tools.logging_dec import logging_check
from django.core.cache import cache
from tools.sms import YunTongXin
from django.conf import settings
from .tasks import send_sms_c


# Create your views here.
# 异常码：10100--10199

# django提供了一个装饰器method_decorator，可以将函数装饰器转换成方法装饰器


# FBV 基于函数视图
@logging_check
def user_views(request, username):
    if request.method != 'POST':
        result = {'code': 10107, 'error': '请求有误！'}
        return JsonResponse(result)

    # try:
    #     user = UserProfile.objects.get(username=username)
    # except Exception as e:
    #     result = {'code': 10108, 'error': '用户名或密码有误！！！'}
    #     return JsonResponse(result)
    # 一查
    user = request.myuser
    # 二改
    avatar = request.FILES['avatar']
    user.avatar = avatar
    # 三保存
    user.save()
    return JsonResponse({'code': 200})


# CBV 基于类视图，更灵活[可继承]
class UserViews(View):

    def get(self, request, username=None):

        if username:
            # v1/users/username
            try:
                user = UserProfile.objects.get(username=username)
            except Exception as e:
                result = {'code': 10106, 'error': '用户名或密码错误！'}
                return JsonResponse(result)
            reslut = {'code': 200, 'username': username,
                      'data': {'info': user.info, 'sign': user.sign, 'nickname': user.nickname,
                               'avatar': str(user.avatar)}}
            return JsonResponse(reslut)
        else:
            # v1/users
            pass
        return JsonResponse({'code': 200, 'error': 'test'})

    def post(self, request):
        # 获取数据
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        email = json_obj['email']
        password_1 = json_obj['password_1']
        password_2 = json_obj['password_2']
        phone = json_obj['phone']
        sms_num = json_obj['sms_num']

        # 校验数据
        # 用户信息
        if not all([username, email, password_1, password_2, phone]):
            result = {'code': 10101, 'error': '信息不全！'}
            return JsonResponse(result)
        # 用户名
        if not re.match('^[a-zA-Z0-9]{6,11}$', username):
            result = {'code': 10102, 'error': '用户错误！'}
            return JsonResponse(result)
        # 密码
        if password_1 != password_2:
            result = {'code': 10103, 'error': '密码不一致！'}
            return JsonResponse(result)
        # 手机号
        if not re.match('^1[3456789]\d{9}$', phone):
            result = {'code': 10104, 'error': '手机号不正确！'}
            return JsonResponse(result)

        # 比对验证码是否正确
        old_code = cache.get('sms_%s' % phone)
        if not old_code:
            result = {'code': 10110, 'error': '验证码已过期！'}
            return JsonResponse(result)
        if int(sms_num) != old_code:
            result = {'code': 10111, 'error': '验证码不正确！'}
            return JsonResponse(result)

        # 用户是否可用
        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {'code': 10105, 'error': '用户已存在！'}
            return JsonResponse(result)
        # 密码进行哈希加密
        p_m = hashlib.md5()
        p_m.update(password_1.encode())
        # 插入用户数据
        user = UserProfile.objects.create(username=username, nickname=username, password=p_m.hexdigest(), email=email,
                                          phone=phone)

        return JsonResponse({'code': 200, 'username': username, 'data': {}})

    @method_decorator(logging_check)
    def put(self, request, username=None):
        # 更新用户数据[呢称，个人签名，个人描述]
        json_str = request.body
        json_obj = json.loads(json_str)

        # try:
        #     user = UserProfile.objects.get(username=username)
        # except Exception as e:
        #     result = {'code': 10109, 'error': '用户名或密码有误！！！'}
        #     return JsonResponse(result)
        user = request.myuser

        user.sign = json_obj['sign']
        user.info = json_obj['info']
        user.nickname = json_obj['nickname']

        user.save()
        return JsonResponse({'code': 200})


def sms_views(request):
    if request.method != "POST":
        result = {'code': 10108, 'error': '请求有误！'}
        return JsonResponse(result)
    json_str = request.body
    json_obj = json.loads(json_str)
    phone = json_obj['phone']
    print(phone)
    # 生成验证码
    code = random.randint(1000, 9999)
    print('phone', phone, 'code', code)
    # 存储验证码 django_redis 安装：sudo pip3 install django-redis
    cache_key = 'sms_%s' % phone
    # 检查是否已经有发过的且未过期的验证码
    old_code = cache.get(cache_key)
    if old_code:
        result = {'code': 10109, 'error': '验证码已发送！'}
        return JsonResponse(result)
    cache.set(cache_key, code, 60)
    # 发送验证码 -> 短信
    # send_sms(phone, code)
    # celery版
    send_sms_c.delay(phone, code)

    return JsonResponse({'code': 200})


def send_sms(phone, code):
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
