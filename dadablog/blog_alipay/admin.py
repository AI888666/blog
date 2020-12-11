from django.contrib import admin
from .models import Money
# Register your models here.


class MoneyManger(admin.ModelAdmin):
    list_display = ['id', 'money', 'order_id', 'created_time', 'updated_time', 'is_active', 'topic']
    list_display_links = ['money']


admin.site.register(Money, MoneyManger)
