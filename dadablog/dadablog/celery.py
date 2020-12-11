from celery import Celery, platforms
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dadablog.settings')

app = Celery('dadablog', backend='redis://:@127.0.0.1:6379/6', broker='redis://:@127.0.0.1:6379/8')
# 更新配置
# app.conf.update(
#     BORKER_URL='redis://:@127.0.0.1:6379/6'
# )
# app.config_from_object('django.conf:settings')
# app.conf.broker_url = 'redis://localhost:6379'
# app.conf.broker_transport_options = {'visibility_timeout': 43200}

# 自动去注册应用下寻找加载worker函数
app.autodiscover_tasks(settings.INSTALLED_APPS)


platforms.C_FORCE_ROOT = True

# celery -A dadablog worker -l info
