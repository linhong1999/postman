# -*- coding: utf-8 -*-
from django.contrib import auth
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework import status as http_status

from commonapi import serializers
from commonapi.commonresponse import CommonResponse
from . import models


class LoginRegister(ObtainJSONWebToken, CreateModelMixin, GenericViewSet):
    serializer_class = serializers.UserModelSerializers

    def login(self, req, *args, **kwargs):
        """
        登录接口
        @api {POST} /userapi/v1/login/
        @apiName userapi

        @apiParam {String} username    用户名
        @apiParam {String} get_sex     性别
        @apiParam {String} img         头像
        @apiSuccess Example {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "result": true,
            "status": 200,
            "message": "success",
            "data": {
                "token": "xxxx.xxxx.xxxx",
                "user_info": {
                    "username": "lh",
                    "get_sex": "male",
                    "img": "/media/img/default.png"
                }
            }
        }
        """
        response = super().post(req, *args, **kwargs)
        if response:
            response.data['data'] = serializers.UserModelSerializers(
                models.User.objects.get(username=req.data.get('username'))
            ).data
        return CommonResponse(response.data)

    def register(self, req, *args, **kwargs):
        """
        注册接口
        @api {POST} /userapi/v1/register/
        @apiName userapi

        @apiParam {String} username    用户名
        @apiParam {String} get_sex     性别
        @apiParam {String} img         头像
        @apiSuccess Example {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "result": true,
            "status": 200,
            "message": "注册成功",
            "data": {
                "username": "林二",
                "get_sex": "male",
                "img": "http://127.0.0.1:8000/media/img/default.png"
            }
        }
        """
        class RegisterCode:
            SUCCESS = http_status.HTTP_201_CREATED
            USER_EXISTS = http_status.HTTP_202_ACCEPTED
            PWD_NOT_MATCH = http_status.HTTP_202_ACCEPTED

        def validate(attrs):
            if models.User.objects.filter(username=attrs.get('username')).first():
                return RegisterCode.USER_EXISTS, "用户已存在"
            re_pwd = attrs.get('re_pwd')
            attrs.pop('re_pwd')
            if re_pwd is None:
                return RegisterCode.PWD_NOT_MATCH, '请重复输入密码'
            if re_pwd != attrs.get('password'):
                return RegisterCode.PWD_NOT_MATCH, '两次密码不匹配'

            return RegisterCode.SUCCESS, "注册成功"

        status_code, msg = validate(req.data)
        if status_code != RegisterCode.SUCCESS:
            return CommonResponse(status=status_code, message=msg)

        response = self.create(req, *args, **kwargs)
        return CommonResponse(response.data, message=msg)

    def logout(self, req):
        """
        注册接口
        @api {POST} /userapi/v1/register/
        @apiName userapi

        @apiSuccess Example {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "result": true,
            "status": 200,
            "message": "logout successfully",
            "data": null
        }
        """
        auth.logout(req)
        return CommonResponse(message='logout successfully')


class LoginRegister2(CreateModelMixin, GenericAPIView):
    # queryset = models.TestUser.objects.all()
    serializer_class = serializers.UserModelSerializers2

    def post(self, req, *args, **kwargs):
        response = self.create(req, *args, **kwargs)

        return response
