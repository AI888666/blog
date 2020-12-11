from django.contrib import admin
from .models import Message


# Register your models here.

class MessageManger(admin.ModelAdmin):
    list_display = ['id', 'content', 'parent_message', 'publisher', 'topic', 'created_time', 'is_active']


admin.site.register(Message, MessageManger)
