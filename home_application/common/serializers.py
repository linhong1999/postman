# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework_jwt.views import JSONWebTokenSerializer
from .. import models


class UserModelSerializers(JSONWebTokenSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('username', 'password', 'get_sex', 'sex', 'img')
        extra_kwargs = {
            'sex': {
                'write_only': True,
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
        model = models.TestUser
        fields = ('username', 'password', 'sex')
        extra_kwargs = {
            'sex': {
                'write_only': True,
            },
        }


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ('username', 'user_img', 'comment', 'create_time', 'id', 'pyq_obj_id')


class WinkModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wink
        fields = ('username',)


class PyqModelSerializers(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    winks = serializers.SerializerMethodField()

    class Meta:
        model = models.Pyq
        fields = ('username', 'user_img', 'id', 'content', 'comments', 'create_time', 'winks')
        extra_kwargs = {
            'content': {
                'max_length': 255,
                'error_messages': {
                    'max_length': '超出长度限制!',
                },
            },
            'user': {
                'write_only': True
            },

        }

    def get_comments(self, obj):
        # 正向查询
        comment_ser = CommentModelSerializer(obj.comment_set.filter(is_delete=False), many=True).data
        return comment_ser

    def get_winks(self, obj):
        wink_ser = obj.wink_set.filter(is_delete=False)
        wink_list = [obj.user.username for obj in wink_ser]
        return wink_list

