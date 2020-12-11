from celery import Celery

app = Celery('xuan_result',
             broker='redis://:@127.0.0.1:6379/3',
             backend='redis://:@127.0.0.1:6379/4'
             )


@app.task
def task_test(a, b):
    print('task is running...')
    return a + b
# 启动
# celery -A tasks_result worker --loglevel=info
# celery -A tasks_result worker -l info


# from tasks_result import task_test
# task_test.delay(10,99)
