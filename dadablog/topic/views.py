import json

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from blog_alipay.models import Money
from message.models import Message
from tools.logging_dec import logging_check, get_user_by_request

# Create your views here.
from topic.models import Topic
from user.models import UserProfile
from tools.cache_dec import cache_set


class TopicViews(View):

    def clear_topics_caches(self, request):
        # 删除缓存
        path = request.path_info
        cache_key_p = ['topics_cache_self_', 'topics_cache_']
        cache_key_h = ['', '?category=tec', '?=category=no-tec']
        all_keys = []
        for key_p in cache_key_p:
            for key_h in cache_key_h:
                all_keys.append(key_p + path + key_h)
        print('clear caches is', all_keys)
        cache.delete_many(all_keys)

    def make_topic_res(self, author, author_topic, is_self):
        """
            具体博客的响应格式
        :param author: 作者
        :param author_topic:　作者博客
        :param is_self: 是否为博主
        :return: 具体博客
        """
        if is_self:
            # 博主 下一篇文章，上一篇文章
            next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author).first()
            last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author).last()
        else:
            # 访客 下一篇文章，上一篇文章
            next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author, limit='public').first()
            last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author, limit='public').last()

        # 下一个文章上一个文章的id和title
        next_id = next_topic.id if next_topic else None
        next_title = next_topic.title if next_topic else ''
        last_id = last_topic.id if last_topic else None
        last_title = last_topic.title if last_topic else ''

        # 关联留言回复
        all_message = Message.objects.filter(topic=author_topic).order_by('-created_time')
        # print('all_message ----->', all_message)

        msg_list = []  # 留言内容
        res_dic = {}  # 留言的对应回复内容
        m_count = 0
        for msg in all_message:
            if msg.parent_message:
                # 回复
                res_dic.setdefault(msg.parent_message, [])
                res_dic[msg.parent_message].append({
                    'msg_id': msg.id,
                    'publisher': msg.publisher.nickname,
                    'publisher_avatar': str(msg.publisher.avatar),
                    'content': msg.content
                })
                pass
            else:
                # 留言
                m_count += 1
                msg_list.append({
                    'id': msg.id,
                    'content': msg.content,
                    'publisher': msg.publisher.nickname,
                    'publisher_avatar': str(msg.publisher.avatar),
                    'created_time': msg.created_time.strftime('%Y-%m-%d %H-%M-%S'),
                    'reply': []
                })
        for m in msg_list:
            if m['id'] in res_dic:
                m['reply'] = res_dic[m['id']]

        res = {'code': 200, 'data': {}}
        res['data']['nickname'] = author.nickname
        res['data']['title'] = author_topic.title
        res['data']['category'] = author_topic.category
        res['data']['created_time'] = author_topic.created_time.strftime('%Y-%m-%d %H-%M-%S')
        res['data']['content'] = author_topic.content
        res['data']['introduce'] = author_topic.introduce
        res['data']['author'] = author.username
        res['data']['next_id'] = next_id
        res['data']['next_title'] = next_title
        res['data']['last_id'] = last_id
        res['data']['last_title'] = last_title
        res['data']['messages'] = msg_list
        res['data']['messages_count'] = m_count
        return res

    def make_topics_res(self, author, author_topics):
        """
            返回博客列表对象格式
        :param author: 作者对象
        :param author_topics: 作者博客
        :return:
        """
        res = {'code': 200, 'data': {}}
        topics_res = []
        for topic in author_topics:
            d = {}
            d['id'] = topic.id
            d['title'] = topic.title
            d['category'] = topic.category
            d['created_time'] = topic.created_time.strftime('%Y-%m-%d %H-%M-%S')
            d['introduce'] = topic.introduce
            d['author'] = author.nickname
            topics_res.append(d)
        res['data']['topics'] = topics_res
        res['data']['nickname'] = author.nickname
        return res

    @method_decorator(cache_set(300))
    def get(self, request, author_id):
        """
            self: 对象自己
        :param request: 请求对象
        :param author_id: 作者对象
        :return:　所有文章
        """
        # /v1/topic/username
        # 访问者　visitor
        # 博主
        print('views_in ......')
        try:
            author = UserProfile.objects.get(username=author_id, is_active=True)
        except Exception as e:
            result = {'code': 10302, 'error': '作者不存在！'}
            return JsonResponse(result)
        # 访问者，没有登录
        # 博主，登录　公开文章　＋　个人文章
        # 不是博主，登录　公开文章
        visitor = get_user_by_request(request)
        visitor_username = None
        if visitor:
            visitor_username = visitor.username

        # 获取文章编号 id
        t_id = request.GET.get('t_id')
        if t_id:
            # 获取指定文章列表
            # v1/topics/username/t_id
            t_id = int(t_id)
            is_self = False
            if visitor_username == author_id:
                # 获取博主自己文章
                is_self = True
                try:
                    author_topic = Topic.objects.get(id=t_id, author_id=author_id, is_active=False)
                except Exception as e:
                    result = {'code': 10303, 'error': 'not is topic'}
                    return JsonResponse(result)
            else:
                # 访客获取文章
                try:
                    author_topic = Topic.objects.get(id=t_id, author_id=author_id, is_active=False, limit='public')
                except Exception as e:
                    result = {'code': 10303, 'error': 'not is topic'}
                    return JsonResponse(result)
            # 构建具体博客的响应格式
            res = self.make_topic_res(author, author_topic, is_self)
            return JsonResponse(res)

        else:  # 获取博客文章列表
            # 查看有无查询字符串
            category = request.GET.get('category')

            if category in ['tec', 'no-tec']:
                if visitor_username == author_id:
                    # 博主自己访问自己的博客
                    author_topics = Topic.objects.filter(author_id=author_id, is_active=False, category=category)
                else:
                    author_topics = Topic.objects.filter(author_id=author_id, is_active=False, limit='public',
                                                         category=category)
            else:
                if visitor_username == author_id:
                    # 博主自己访问自己的博客
                    author_topics = Topic.objects.filter(author_id=author_id, is_active=False)
                else:
                    author_topics = Topic.objects.filter(author_id=author_id, is_active=False, limit='public')
            # 加载响应格式
            res = self.make_topics_res(author, author_topics)
            return JsonResponse(res)

    @method_decorator(logging_check)
    def post(self, request, author_id):
        """
            创建博客
        :param request: 请求对象
        :param author_id: 创建者对象
        :return:
        """
        # 没有发博客
        # 获取当前用户
        author = request.myuser
        # １．获取数据
        json_str = request.body
        json_obj = json.loads(json_str)
        title = json_obj['title']
        category = json_obj['category']
        content = json_obj['content']
        content_text = json_obj['content_text']
        introduce = content_text[:30]
        limit = json_obj['limit']
        # ２．校验
        # 权限校验：公开／私有
        if limit not in ['public', 'private']:
            result = {'code': 10300, 'error': '权限有误！'}
            return JsonResponse(result)
        # 技术分类校验：技术／非技术
        if category not in ['tec', 'no-tec']:
            result = {'code': 10301, 'error': '技术分类有误！'}
            return JsonResponse(result)
        # ３．创建topic数据
        Topic.objects.create(
            title=title,
            content=content,
            limit=limit,
            category=category,
            introduce=introduce,
            author=author
        )
        # 清楚缓存
        self.clear_topics_caches(request)
        # ４．返回相应
        return JsonResponse({'code': 200})

    @method_decorator(logging_check)
    def delete(self, request, author_id):
        try:
            author = UserProfile.objects.get(username=author_id, is_active=True)
        except Exception as e:
            result = {'code': 10302, 'error': '作者不存在！'}
            return JsonResponse(result)
        # 获取文章编号 id
        t_id = request.GET.get('t_id')
        if t_id:
            # 获取指定文章列表
            # v1/topics/username/t_id
            t_id = int(t_id)
            # 获取博主自己文章
            try:
                author_topic = Topic.objects.get(id=t_id, author_id=author_id, is_active=False)
            except Exception as e:
                result = {'code': 10304, 'error': 'not is topic'}
                return JsonResponse(result)
            author_topic.is_active = True
            author_topic.save()
            result = {'code': 200, 'data': {}}
            return JsonResponse(result)
        else:
            result = {'code': 10308, 'error': '没有删除权限！'}
            return JsonResponse(result)

    # def patch(self, request, author_id):
    #     pass
