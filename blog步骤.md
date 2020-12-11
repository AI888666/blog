# **blog项目**

## 前后端分离

​    目前传递过来的是json格式数据，获取数据：request.body
​    通信数据格式：json
​    跨域解决方案：token

## 用户系统

### 注册：

```markdown
1. 获取数据json格式：request.body
    1.1 获取数据是json格式
    1.2 将数据转为python格式 json.loads() ---> {}
    1.3获取具体数据
2. 校验数据 (数据合法性，一定要做 防止通过测试工具或者脚本进行操作)
    2.1 数据是否全面 all([username, password_1,...])
    2.2 校验用户名
    2.3 两次密码是否一致
    2.4 手机号
    2.5 用户名是否可用
    2.6 对比验证码正确性
        from django.core.cache import cache
        old_code = cache.get(cache_key)
        2.6.1 验证码过期
        2.6.2 验证码错误
 3. 处理数据 (插入用户信息，密码进行加密)
        3.1 数据加密 hashlib.md5()
        3.2 模型类.objects.create()
        3.3 并发问题
4. 响应内容
        4.1 响应数据格式 json
        
```


### 短信验证码：

~~~markdown
    使用 容联云 三方通信
    1. 文档的学习
    2. 代码功能的实现 file: tools/sms.py
    3. 结合 django 发送短信
        3.1 生成验证码 code = random.randint(1000, 9999)
        3.2 存储验证码：
            from django.core.cache import cache
            cache_key (格式：sms_phone)
            cache.set(cache_key, code, 120)
        3.3 发送短信
            3.3.1 调用 封装的 send_sms
            3.3.2 应用celery分布式发送短信　send_sms_c
            
            
~~~



~~~markdown
跨域:
    同源策略:
        协议 域名 端口号

    django-cors-headers
    
token组成：
    header: 算法、 token 类型
    payload: 公有声明 私有声明
    签名: 校验数据
~~~



### 登录：

~~~markdown
1. 获取数据

2. 校验数据(查询用户)

3. 返回响应

~~~



### 回话保持：

~~~markdown

    1. 封装 logging_check (file: tools/logging_dec.py)
    2. 使用：
        from django.utils.decorators import method_decorator
        method_decorator(logging_check) # 将试图函数的装饰器转为 方法装饰器
~~~

