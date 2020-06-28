# -*- coding: utf-8 -*-
from django.contrib import auth
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.views import ObtainJSONWebToken
from CommonAPI import serializers
from CommonAPI.MyResponse import MyResponse
from UserAPI import models


class LoginRegister(ObtainJSONWebToken, CreateModelMixin, GenericViewSet):
    serializer_class = serializers.UserModelSerializers

    def login(self, req, *args, **kwargs):
        response = super().post(req, *args, **kwargs)
        if response:
            response.data['user_info'] = serializers.UserModelSerializers(
                models.User.objects.get(username=req.data.get('username'))
            ).data

        return response

    def register(self, req, *args, **kwargs):
        # 自定义注册
        def validate(attrs):
            if models.User.objects.filter(username=attrs.get('username')).first():
                return -1, "用户已存在"
            re_pwd = attrs.get('re_pwd')
            attrs.pop('re_pwd')
            if re_pwd is None:
                return -1, '请重复输入密码'
            if re_pwd != attrs.get('password'):
                return -1, '两次密码不匹配'

            return 1, "注册成功"

        status_code, msg = validate(req.data)
        if status_code != 1:
            return MyResponse(status_code, msg)

        return self.create(req, *args, **kwargs)

    def logout(self, req):
        auth.logout(req)
        # req.session.flush()
        return MyResponse(200, 'logout successfully')


class LoginRegister2(CreateModelMixin, GenericAPIView):
    # queryset = models.TestUser.objects.all()
    serializer_class = serializers.UserModelSerializers2

    def post(self, req, *args, **kwargs):
        response = self.create(req, *args, **kwargs)

        return response