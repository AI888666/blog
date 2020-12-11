from django.contrib import admin
from .models import UserProfile


# Register your models here.


class UserManger(admin.ModelAdmin):
    # list_display = ['username', 'email', 'phone', 'nickname', 'password', 'avatar', 'sign', 'info', 'created_time',
    #                 'updated_time', 'is_active']
    list_display = ['username', 'email', 'phone', 'nickname', 'created_time', 'updated_time', 'is_active']


admin.site.register(UserProfile, UserManger)
