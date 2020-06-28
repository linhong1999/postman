# -*- coding: utf-8 -*-

from rest_framework import serializers, exceptions
from rest_framework_jwt.views import JSONWebTokenSerializer
from UserAPI import models as user_api_model
from PyqAPI import models as pyq_api_model


class UserModelSerializers(JSONWebTokenSerializer, serializers.ModelSerializer):

    class Meta:
        model = user_api_model.User
        fields = ('username', 'password', 'get_sex', 'sex', 'img')
        extra_kwargs = {
            'username': {
                'max_length': 10,
                'error_messages': {
                    'max_length': '太长',
                }
            },
            'sex': {
                'write_only': True,
                # 'required': True
            },
        }

    def validate(self, attrs):
        path = self.context.get('request').path
        if path.split('/')[3] == 'register':
            return attrs
        else:
            return super().validate(attrs)


class UserModelSerializers2(serializers.ModelSerializer):

    class Meta:
        model = user_api_model.TestUser
        fields = ('username', 'password', 'sex')
        extra_kwargs = {
            'username': {
                'max_length': 10,
                'error_messages': {
                    'max_length': '太长',
                }
            },
            'sex': {
                'write_only': True,
            },
        }


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = pyq_api_model.Comment
        fields = ('username', 'user_img', 'comment', 'create_time', 'pyq_obj')


class WinkModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = pyq_api_model.Wink
        fields = ('username',)


class PyqModelSerializers(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    winks = serializers.SerializerMethodField()
    class Meta:
        model = pyq_api_model.Pyq
        fields = ('username', 'user_img', 'id', 'content', 'comments', 'create_time', 'winks')
        extra_kwargs = {
            'content': {
                'max_length': 255,
                'error_messages': {
                    'max_length': '超出长度限制!',
                },
            },
            'user_id': {
                'write_only': True
            },

        }

    def get_comments(self, obj):
        # 正向查询
        comment_ser = CommentModelSerializer(obj.comment_set.only('comment'), many=True).data
        return comment_ser

    def get_winks(self, obj):
        # wink_ser = WinkModelSerializer(obj.wink_set.filter(is_delete=False),many=True).data
        wink_ser = obj.wink_set.filter(is_delete=False)
        wink_list = [obj.user.username for obj in wink_ser]
        return wink_list

