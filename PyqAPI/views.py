# -*- coding: utf-8 -*-
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from CommonAPI import serializers, MyResponse
from . import models


class PyqBrowser(RetrieveModelMixin, ListModelMixin, GenericViewSet):

    serializer_class = serializers.PyqModelSerializers
    def sort_by_date(self, query):
        date_set = set()
        sored_query_dict = dict()
        for obj in query:
            date_split = obj.get('create_time')[:10].split('-')
            date_tuple = '%s-%s-%s' % (date_split[0], date_split[1], date_split[2])
            date_set.add(date_tuple)
            if date_tuple not in sored_query_dict:
                sored_query_dict = {}.fromkeys(date_set, [])
            sored_query_dict[date_tuple].append(obj)

        return sored_query_dict
    def get_pyq(self, req, *args, **kwargs):
        # 获取 朋友圈 单查，群查
        self.queryset = models.Pyq.objects.filter(is_delete=False)
        pk = kwargs.get('pk')
        if pk:
            response = self.retrieve(req, *args, **kwargs)
        else:
            response = self.list(req, *args, **kwargs)

        response.data = self.sort_by_date(response.data)
        return response

    def get_private_pyq_zone(self, req, *args, **kwargs):
        # 访问一个人的空间 群查
        user_name = kwargs.get('user_name')
        self.queryset = models.Pyq.objects.filter(user__username=user_name, is_delete=False)
        response = self.list(req, *args, **kwargs)
        return response

    def test(self, req, *args, **kwargs):
        print(kwargs)
        print(req)
        return Response({
            'msg': 'request ok'
        })

class PyqOperator(RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    pyq_queryset = models.Pyq.objects.filter(is_delete=False)
    comment_queryset = models.Comment.objects.filter(is_delete=False)
    serializer_class = serializers.PyqModelSerializers
    # 获取 token
    authentication_classes = [JSONWebTokenAuthentication]
    # 只有拥有有效的 token 的用户才能操作
    permission_classes = [IsAuthenticated]

    def test(self, req, *args, **kwargs):
        print(kwargs)
        print(req)
        return Response({
            'msg': 'request ok'
        })

    def add_pyq(self, req, *args, **kwargs):
        # 发表一条动态
        req.data['user'] = req.user.id
        models.Pyq(
            user= req.user,
            content=req.data['content']
        ).save()
        # response = self.create(req, *args, **kwargs)
        # Column 'user_id' cannot be null
        return Response({
            'msg': '发表成功'
        })

    def add_comment(self, req, *args, **kwargs):
        # 评论某条动态
        self.serializer_class = serializers.CommentModelSerializer
        req.data['user'] = req.user.id
        req.data['pyq_obj'] = kwargs.get('pyq_obj_id')

        models.Comment(
            pyq_obj_id=kwargs.get('pyq_obj_id'),
            user=req.user,
            comment=req.data['comment']
        ).save()
        # Column 'user_id' cannot be null
        # return self.create(req, *args, **kwargs)
        return Response({
            'msg': '评论成功'
        })

    def update_pyq(self, req, *args, **kwargs):
        # 更新朋友圈
        self.queryset = self.pyq_queryset
        response = self.update(req, *args, **kwargs)
        return response

    def del_restore_pyq(self, req, *args, **kwargs):
        # 删除或恢复朋友圈
        pyq_user_name = kwargs.get('pyq_user_name')
        pk = req.data.get('pk')
        method = req.data.get('method')
        is_delete = True if method == 'del' else False
        if pyq_user_name == req.user.username:
            # 级联
            models.Pyq.objects.filter(pk=pk).update(is_delete=is_delete)
            models.Comment.objects.filter(pyq_obj_id=pk).update(is_delete=is_delete)

        return Response({
            'status_code': 1,
            'msg': '%s成功' % ('删除' if method == 'del' else '恢复')
        })

    def del_comment(self, req, *args, **kwargs):
        # 删除评论
        self.queryset = self.comment_queryset
        comment_obj_id = kwargs.get('comment_obj_id')
        models.Comment.objects.filter(pk=comment_obj_id).update(is_delete=True)

        return Response({
            'status_code': 1,
            'msg': '删除成功'
        })

    def update_wink_status(self, req, *args, **kwargs):
        # 点赞
        user_id = req.user.id
        pyq_obj_id = req.data.get('pyq_obj_id')
        # 这样空值 也为 True
        obj = models.Wink.objects.filter(pyq_obj_id=pyq_obj_id, user_id=user_id).first()

        if obj:
            obj.is_delete = not obj.is_delete
            obj.save()
        else:
            models.Wink(
                user_id=user_id, pyq_obj_id=pyq_obj_id, is_delete=True
            ).save()

        return Response({
            'status': 200,
        })
    # def delete(self, req, *args, **kwargs):
    #     pk = kwargs.get('pk')
    #     if pk:
    #         models.Pyq.objects.filter(pk=pk).update(is_delete=False)
    #         status_code, msg = 1, "删除成功"
    #     else:
    #         status_code, msg = -1, "对象不存在"
    #
    #     return MyResponse(status_code, msg)

