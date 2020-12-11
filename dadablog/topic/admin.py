from django.contrib import admin
from .models import Topic


# Register your models here.
class TopicManger(admin.ModelAdmin):
    # list_display = ['id', 'title', 'category', 'limit', 'introduce', 'content', 'created_time', 'updated_time',
    #                 'is_active', 'author']
    list_display = ['id', 'title', 'category', 'limit','created_time', 'updated_time', 'is_active', 'author']
    list_display_links = ['title']



admin.site.register(Topic, TopicManger)
