from celery import Celery

app =Celery('xuan',
            broker='redis://:@127.0.0.1:6379/7',
            #broker='redis://:123456@127.0.0.1:6379/7',#有密码
            )


@app.task
def task_test():
    print('task is running...')

# 启动
# celery -A tasks worker -l info

