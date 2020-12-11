import random

from django.db import models


# Create your models here.


def default_sign():
    signs = ['来吧，兄弟', '奔跑吧，兄弟', '键盘敲难，年薪百万', '上吧，大兄弟']
    return random.choice(signs)


class UserProfile(models.Model):
    username = models.CharField(max_length=11, verbose_name='用户名', primary_key=True)
    nickname = models.CharField(max_length=30, verbose_name='呢称')
    password = models.CharField(max_length=32, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
    phone = models.CharField(max_length=11, verbose_name='手机号')
    avatar = models.ImageField(upload_to='avatar', null=True, verbose_name='头像')
    sign = models.CharField(max_length=50, verbose_name='个人签名', default=default_sign)
    info = models.CharField(max_length=150, verbose_name='个人简介', default='')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(verbose_name='是否活跃', default=True)

    class Meta:
        db_table = 'user_user_profile'
        verbose_name = '用户列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
