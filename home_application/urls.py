# -*- coding: utf-8 -*-
from django.conf.urls import url
from rest_framework_jwt.views import ObtainJSONWebToken

from .api import pyq_api, user_api

urlpatterns = [
    url(r'^pyq_api/v1/anno_pyq/$', pyq_api.PyqBrowser.as_view({'get': 'get_pyq'})),
    url(r'^pyq_api/v1/private_pyq_zone/(?P<user_name>.*)/$',
        pyq_api.PyqBrowser.as_view({'get': 'get_private_pyq_zone'})),
    url(r'^pyq_api/v1/pyq_operate/$', pyq_api.PyqOperator.as_view({'post': 'add_pyq'})),
    url(r'^pyq_api/v1/pyq_operate/(?P<pk>.*)/$', pyq_api.PyqOperator.as_view({
        'delete': 'del_restore_pyq',
        'put': 'update_pyq',
        'post': 'update_wink_status'
    })),
    url(r'^pyq_api/v1/comment_operate/(?P<pyq_obj_id>.*)/(?P<comment_obj_id>.*)$',
        pyq_api.PyqOperator.as_view({'post': 'add_comment', 'delete': 'del_comment'})),

    url(r'^user_api/v1/login/$', user_api.LoginRegister.as_view({'post': 'login'})),
    url(r'^user_api/v2/login/$', ObtainJSONWebToken.as_view()),
    url(r'^user_api/v1/logout/$', user_api.LoginRegister.as_view({'post': 'logout'})),
    url(r'^user_api/v1/register/$', user_api.LoginRegister.as_view({'post': 'register'})),
    url(r'^user_api/v2/register/$', user_api.LoginRegister2.as_view()),
]

