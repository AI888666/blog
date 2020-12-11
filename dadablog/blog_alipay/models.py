from django.db import models
from topic.models import Topic
# Create your models here.


class Money(models.Model):
    money = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='总余额')
    order_id = models.CharField(max_length=50, verbose_name='打赏订单号')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(verbose_name='是否有余额', default=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='打赏的文章')

    class Meta:
        verbose_name = '总余额列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.money