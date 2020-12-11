from django.db import models
from user.models import UserProfile

# Create your models here.
# 1. 后端给前端文章全部内容，前端自己截取
# ２. 后端给数据库里获取文章全部内容，获取好后，响应给前端
# ３. 数据库冗余一个字段(简介)，后端只读取简介字段内容


class Topic(models.Model):
    title = models.CharField(verbose_name='文章标题', max_length=50)
    category = models.CharField(verbose_name='文章分类', max_length=20)
    limit = models.CharField(verbose_name='文章权限', max_length=20)
    introduce = models.CharField(verbose_name='文章简介', max_length=30)
    content = models.TextField(verbose_name='文章内容')

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(verbose_name='是否删除文章', default=False)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='作者')

    class Meta:
        verbose_name = '博客列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

