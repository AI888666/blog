from django.db import models
from user.models import UserProfile
from topic.models import Topic


# Create your models here.
class Message(models.Model):
    content = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)
    parent_message = models.IntegerField(verbose_name='回复的留言id')
    publisher = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name='是否删除留言', default=False)

    class Meta:
        verbose_name = '留言列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.parent_message

