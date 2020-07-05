# -*- coding: utf-8 -*-
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from commonapi import serializers
from commonapi.commonresponse import CommonResponse
from . import models


class PyqBrowser(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = serializers.PyqModelSerializers

    def sort_by_date(self, query):
        sored_query_dict = dict()
        for obj in query:
            date_split = obj.get('create_time')[:10].split('-')
            date_tuple = '%s-%s-%s' % (date_split[0], date_split[1], date_split[2])
            if date_tuple not in sored_query_dict:
                sored_query_dict[date_tuple] = []
            sored_query_dict[date_tuple].append(obj)

        return sored_query_dict

    def get_pyq(self, req, *args, **kwargs):
        """
        获取 朋友圈 群查
        @api {GET} /pyqapi/v1/anno_pyq/
        @apiName pyqapi

        @apiParam {String} 2020-06-28   分类日期
        @apiParam {String} username     用户名
        @apiParam {String} user_img     用户头像
        @apiParam {int} id              item_id
        @apiParam {String} content      朋友圈内容
        @apiParam {String} comments     评论
        @apiParam {String} create_time  创建日期
        @apiParam {String} winks        点赞列表
        @apiSuccess Example {json} Success-Response:
        HTTP/1.1 200 OK
        {
        "result": true,
        "status": 200,
        "message": "success",
        "data": {
            "2020-06-28": [
                {
                    "username": "lh",
                    "user_img": "img/default.png",
                    "id": 1,
                    "content": "今天周天",
                    "comments": [
                        {
                            "username": "qqq",
                            "user_img": "img/default.png",
                            "comment": "123",
                            "create_time": "2020-06-28T12:18:30.218048Z",
                            "id": 11
                        }
                    ],
                    "create_time": "2020-06-28T03:10:58.158869Z",
                    "winks": [
                        "lh",
                        "qqq"
                    ]
                },
                {
                    "username": "lh",
                    "user_img": "img/default.png",
                    "id": 8,
                    "content": "dsad",
                    "comments": [],
                    "create_time": "2020-06-28T13:56:09.049968Z",
                    "winks": []
                }
            ]
                }

        获取 朋友圈 单查
        @api {GET} /pyqapi/v1/anno_pyq/(?P<pk>.*)/
        {
            "result": true,
            "status": 200,
            "message": "success",
            "data": {
                "username": "lh",
                "user_img": "img/default.png",
                "id": 1,
                "content": "今天周天",
                "comments": [
                    {
                        "username": "qqq",
                        "user_img": "img/default.png",
                        "comment": "123",
                        "create_time": "2020-06-28T12:18:30.218048Z",
                        "id": 11
                    },
                    {
                        "username": "lh",
                        "user_img": "img/default.png",
                        "comment": "asd",
                        "create_time": "2020-06-28T13:56:23.038339Z",
                        "id": 15
                    }
                ],
                "create_time": "2020-06-28T03:10:58.158869Z",
                "winks": [
                    "lh",
                    "qqq"
                ]
            }
        }
        """
        self.queryset = models.Pyq.objects.filter(is_delete=False)
        pk = kwargs.get('pk')
        if pk:
            response = self.retrieve(req, *args, **kwargs)
        else:
            response = self.list(req, *args, **kwargs)
            response.data = self.sort_by_date(response.data)

        return CommonResponse(response.data)

    def get_private_pyq_zone(self, req, *args, **kwargs):
        """
        访问一个人的空间 群查
        @api {GET} /pyqapi/v1/private_pyq_zone/(?P<user_name>.*)/
        @apiName pyqapi

        @apiParam {String} 2020-06-28   分类日期
        @apiParam {String} username     用户名
        @apiParam {String} user_img     用户头像
        @apiParam {int} id              item_id
        @apiParam {String} content      朋友圈内容
        @apiParam {String} comments     评论
        @apiParam {String} create_time  创建日期
        @apiParam {String} winks        点赞列表
        @apiSuccess Example {json} Success-Response:
        HTTP/1.1 200 OK
        {
        "result": true,
        "status": 200,
        "message": "success",
        "data": [
            {
                "username": "lh",
                "user_img": "img/default.png",
                "id": 1,
                "content": "今天周天",
                "comments": [
                    {
                        "username": "qqq",
                        "user_img": "img/default.png",
                        "comment": "123",
                        "create_time": "2020-06-28T12:18:30.218048Z",
                        "id": 11
                    },
                    {
                        "username": "lh",
                        "user_img": "img/default.png",
                        "comment": "asd",
                        "create_time": "2020-06-28T13:56:23.038339Z",
                        "id": 15
                    }
                ],
                "create_time": "2020-06-28T03:10:58.158869Z",
                "winks": [
                    "lh",
                    "qqq"
                ]
            }
        ]
        """
        user_name = kwargs.get('user_name')
        self.queryset = models.Pyq.objects.filter(user__username=user_name, is_delete=False)
        response = self.list(req, *args, **kwargs)
        return CommonResponse(response.data)


class PyqOperator(RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    pyq_queryset = models.Pyq.objects.filter(is_delete=False)
    comment_queryset = models.Comment.objects.filter(is_delete=False)
    serializer_class = serializers.PyqModelSerializers
    # 获取 token
    authentication_classes = [JSONWebTokenAuthentication]
    # 只有拥有有效的 token 的用户才能操作
    permission_classes = [IsAuthenticated]

    def add_pyq(self, req, *args, **kwargs):
        """
        发表一条动态
        @api {POST} /pyqapi/v1/pyq_operate/
        @apiName pyqapi

        @apiParam {String} username     用户名
        @apiParam {String} user_img     用户头像
        @apiParam {int} id              item_id
        @apiParam {String} content      朋友圈内容
        @apiParam {String} comments     评论
        @apiParam {String} create_time  创建日期
        @apiParam {String} winks        点赞列表
        @apiSuccess Example {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "result": true,
            "status": 200,
            "message": "success",
            "data": {
                "username": "lh",
                "user_img": "img/default.png",
                "id": 14,
                "content": "今天天气好热",
                "comments": [],
                "create_time": "2020-07-04T12:06:56.019547Z",
                "winks": []
            }
        }
        """
        pyq_obj = models.Pyq.objects.create(
            user=req.user,
            content=req.data['content']
        )
        response = self.serializer_class(instance=pyq_obj)
        return CommonResponse(response.data)

    def del_restore_pyq(self, req, *args, **kwargs):
        """
        删除或恢复朋友圈
        @api {DELETE} /pyqapi/v1/pyq_operate/(?P<pk>.*)/
        @apiName pyqapi

        @apiSuccess Example {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "result": true,
            "status": 200,
            "message": "删除成功",
            "data": null
        }
        """
        pk = kwargs.get('pk')
        method = req.method
        is_delete = True if method == 'DELETE' else False
        if req.user:
            # 级联
            models.Pyq.objects.filter(pk=pk).update(is_delete=is_delete)
            models.Comment.objects.filter(pyq_obj_id=pk).update(is_delete=is_delete)

        return CommonResponse(message='%s成功' % ('删除' if method == 'DELETE' else '恢复'))

    def update_pyq(self, req, *args, **kwargs):
        """
        更新朋友圈
        @api {PUT} /pyqapi/v1/comment_operate/(?P<pk>.*)/
        @apiName pyqapi

        @apiParam {String} username     用户名
        @apiParam {String} user_img     用户头像
        @apiParam {int} id              朋友圈id
        @apiParam {String} comments     评论
        @apiParam {String} create_time  创建日期
        @apiParam {String} winks        点赞列表
        @apiSuccess Example {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "result": true,
            "status": 200,
            "message": "success",
            "data": {
                "username": "lh",
                "user_img": "img/default.png",
                "id": 12,
                "content": "2020.6.18",
                "comments": [],
                "create_time": "2020-07-04T12:05:17.858114Z",
                "winks": []
            }
        }
        """
        self.queryset = self.pyq_queryset
        response = self.update(req, *args, **kwargs)
        return CommonResponse(response.data)

    def update_wink_status(self, req, *args, **kwargs):
        """
        点赞
        @api {POST} /pyqapi/v1/pyq_operate/(?P<pk>.*)/
        @apiName pyqapi

        @apiSuccess Example {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "result": true,
            "status": 200,
            "message": "点赞成功",
            "data": null
        }
        """
        user_id = req.user.id
        pyq_obj_id = kwargs.get('pk')
        # 这样空值 也为 True
        obj = models.Wink.objects.filter(pyq_obj_id=pyq_obj_id, user_id=user_id).first()
        if obj:
            obj.is_delete = not obj.is_delete
            is_delete = obj.is_delete
            obj.save()
        else:
            is_delete = False
            models.Wink(
                user_id=user_id, pyq_obj_id=pyq_obj_id, is_delete=is_delete
            ).save()

        return CommonResponse(message='%s成功' % ('取消点赞' if is_delete else '点赞'))

    def add_comment(self, req, *args, **kwargs):
        """
        评论某条动态
        @api {POST} /pyqapi/v1/comment_operate/(?P<pk>.*)/
        @apiName pyqapi

        @apiParam {String} username     用户名
        @apiParam {String} user_img     用户头像
        @apiParam {int} id              评论id
        @apiParam {int} pyq_obj_id      朋友圈id
        @apiParam {String} comments     评论
        @apiParam {String} create_time  创建日期
        @apiParam {String} winks        点赞列表
        @apiSuccess Example {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "result": true,
            "status": 200,
            "message": "success",
            "data": {
                "username": "lh",
                "user_img": "img/default.png",
                "comment": "是啊，真的好热",
                "create_time": "2020-07-04T12:09:35.669831Z",
                "id": 16,
                "pyq_obj_id": "14"
            }
        }
        """
        self.serializer_class = serializers.CommentModelSerializer
        comment_obj = models.Comment.objects.create(
            pyq_obj_id=kwargs.get('pyq_obj_id'),
            user=req.user,
            comment=req.data['comment']
        )
        response = self.serializer_class(instance=comment_obj)
        return CommonResponse(response.data)

    def del_comment(self, req, *args, **kwargs):
        """
        删除评论
        @api {DELETE} /pyqapi/v1/comment_operate/(?P<pyq_obj_id>.*)/(?P<comment_obj_id>.*)
        @apiName pyqapi

        @apiSuccess Example {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "result": true,
            "status": 200,
            "message": "删除成功",
            "data": null
        }
        """
        self.queryset = self.comment_queryset
        comment_obj_id = kwargs.get('comment_obj_id')
        models.Comment.objects.filter(pk=comment_obj_id).update(is_delete=True)
        return CommonResponse(message='删除成功')



