# -*- coding: utf-8 -*-
from django.urls import path, re_path
from . import views
urlpatterns = [
    path('v1/anno_pyq/', views.PyqBrowser.as_view({'get': 'get_pyq'})),
    re_path(r'v1/anno_pyq/(?P<pk>.*)/$', views.PyqBrowser.as_view({'get': 'get_pyq'})),
    re_path(r'v1/private_pyq_zone/(?P<user_name>.*)/$',
            views.PyqBrowser.as_view({'get': 'get_private_pyq_zone'})),
    path('v1/pyq_operate/',
         views.PyqOperator.as_view({'post': 'add_pyq'})),
    re_path(r'v1/pyq_operate/(?P<pk>.*)/$',
            views.PyqOperator.as_view({
                    'delete': 'del_restore_pyq',
                    'put': 'update_pyq',
                    'post': 'update_wink_status'
                })
            ),
    re_path(r'v1/comment_operate/(?P<pyq_obj_id>.*)/(?P<comment_obj_id>.*)$',
            views.PyqOperator.as_view({
                'post': 'add_comment', 'delete': 'del_comment'
            })
            ),
    path('v1/test/', views.PyqOperator.as_view({'post': 'test'})),
    re_path(r'v1/test/(?P<pyq_obj_id>.*)/$',
            views.PyqBrowser.as_view({'post': 'test'})),

]