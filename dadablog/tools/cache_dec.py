from django.core.cache import cache

from .logging_dec import get_user_by_request


def cache_set(expire):
    def _cache_set(func):
        def warpper(request, *args, **kwargs):
            # 区分情景-只做列表页
            if 't_id' in request.GET:
                return func(request, *args, **kwargs)
            # 生成出正确cache_key[访客访问，博主访问]
            # 获取访问者身份
            visitor_user = get_user_by_request(request)
            visitor_username = None
            if visitor_user:
                visitor_username = visitor_user.username
            # 获取博主身份
            author_username = kwargs['author_id']
            print('visitor is %s' % visitor_username)
            print('author is %s' % author_username)
            # 制作cache_key
            # 获取url：request.path_info, request.get_full_path
            full_path = request.get_full_path()
            # 博主：topics_cache_self_full_path
            # 访客：topics_cache_full_path
            if visitor_username == author_username:
                cache_key = 'topics_cache_self_%s' % full_path
            else:
                cache_key = 'topics_cache_%s' % full_path

            # 判断是否有缓存，有缓存直接返回
            res = cache.get(cache_key)
            if res:
                print('cache_in ......')
                return res
            # 执行视图
            res = func(request, *args, **kwargs)
            # 存储缓存
            cache.set(cache_key, res, expire)
            # 返回响应
            return res
        return warpper
    return _cache_set
