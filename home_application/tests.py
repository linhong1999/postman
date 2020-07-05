# -*- coding: utf-8 -*-
from unittest.mock import patch
from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, APITestCase

from .api import user_api, pyq_api
from . import models

VIEW_DICT = {
    'user_api': 'self.user_api_view',
    'pyq_api_anno': 'self.pyq_api_anno_view',
    'pyq_api': 'self.pyq_api_view',
}


def req_resp_handler(self, req_path, api_type, req_dict, method='post', req_data={}):
    request = eval('self.factory.{method}'.format(method=method))(req_path, req_data, format='json')
    view = eval(VIEW_DICT[api_type])
    view = view.as_view(req_dict)
    request.POST._mutable = True
    response = view(request)
    return response


class UserAPITest(TestCase):
    """
    user_api 单元测试
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        models.User.objects.create(username='lh', password='1')
        self.login_data = {
            "username": "lh",
            "password": "1"
        }
        self.register_data = {
            "username": "lh1",
            "password": "1",
            "re_pwd": "1"
        }
        self.user_api_view = user_api.LoginRegister

    def test_register(self):
        response = req_resp_handler(self, '/user_api/v1/register/', 'user_api', {'post': 'register'},
                                    req_data=self.register_data)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = req_resp_handler(self, '/user_api/v1/login/', 'user_api', {'post': 'login'},
                                    req_data=self.login_data)
        self.assertEqual(response.status_code, 200)


class PyqAPITest(APITestCase):
    """
    pyq_api 单元测试
    """
    def setUp(self):
        """先登录获取 token"""
        def token_getter():
            models.User.objects.create(id=1, username='lh', password='1')
            response = self.client.post('/user_api/v1/login/', {"username": "lh", "password": "1"})
            return response.data.get('data').get('token')

        self.factory = APIRequestFactory()
        self.client = Client()
        # 先获取 token
        self.Authorization = {'HTTP_AUTHORIZATION': 'jwt ' + token_getter()}
        # 预加载两条数据
        self.user = models.User.objects.get(id=1)
        models.Pyq.objects.update_or_create(id=1, content='2020.7.5', user=self.user)

        self.pyq_api_anno_view = pyq_api.PyqBrowser
        # 登录用户 才可操作
        self.pyq_api_view = pyq_api.PyqOperator
        self.add_pyq_data = {
            'content': '今天天气好热啊'
        }
        self.update_pyq_data = {
            'content': '2020.7.5'
        }
        self.add_comment_data = {
            "comment": "2020.6.18"
        }

    def test_get_pyq(self):
        response = req_resp_handler(self, '/pyq_api/v1/anno_pyq/', 'pyq_api_anno', {'get': 'get_pyq'}, 'get')
        self.assertEqual(response.status_code, 200)

    def test_get_pyq_pk(self):
        response = req_resp_handler(self, '/pyq_api/v1/anno_pyq/1/', 'pyq_api_anno', {'get': 'get_pyq'}, 'get')
        self.assertEqual(response.status_code, 200)

    def test_get_private_pyq_zone(self):
        response = req_resp_handler(self, '/pyq_api/v1/private_pyq_zone/lh/', 'pyq_api_anno',
                                    {'get': 'get_private_pyq_zone'}, 'get')
        self.assertEqual(response.status_code, 200)

    # mock掉 验证
    # @patch('rest_framework.permissions.IsAuthenticated.has_permission', return_value=True)
    def test_post_pyq_operate(self):
        response = self.client.post('/pyq_api/v1/pyq_operate/', self.add_pyq_data, **self.Authorization)
        self.assertEqual(response.status_code, 200)

    def test_delete_pyq_operate_pk(self):
        response = self.client.delete('/pyq_api/v1/pyq_operate/1/', data={}, **self.Authorization)
        self.assertEqual(response.status_code, 200)

    def test_put_pyq_operate_pk(self):
        response = self.client.put('/pyq_api/v1/pyq_operate/1/', self.update_pyq_data,
                                   content_type='application/json', **self.Authorization)
        self.assertEqual(response.status_code, 200)

    def test_post_pyq_operate_pk(self):
        response = self.client.post('/pyq_api/v1/pyq_operate/1/', data={}, **self.Authorization)
        self.assertEqual(response.status_code, 200)

    def test_post_comment_operate(self):
        response = self.client.post('/pyq_api/v1/comment_operate/1/', self.add_comment_data, **self.Authorization)
        self.assertEqual(response.status_code, 200)

    def test_delete_comment_operate(self):
        response = self.client.post('/pyq_api/v1/comment_operate/1/1', self.add_comment_data, **self.Authorization)
        self.assertEqual(response.status_code, 200)