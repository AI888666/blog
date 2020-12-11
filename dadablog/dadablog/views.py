from django.http import JsonResponse
import logging


def test_cors(request):
    # 创建日志记录器
    # logger = logging.getLogger('dadablog')  # settings.py 中最后的日志器
    # 输出日志
    # logger.info('测试logging模块info')

    return JsonResponse({'msg': 'CORS is OK'})
