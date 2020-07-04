# -*- coding: utf-8 -*-

from rest_framework.authentication import BaseAuthentication


class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 前台在请求头携带认证信息， 默认规范 Authorization 字段携带认证信息
        # 后台固定在请求对象的 META 中获取
        auth = request.META.get('HTTP_AUTHORIZATION')
        # 游客
        if auth is None:
            return None
        return None


