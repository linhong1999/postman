# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework_jwt.views import ObtainJSONWebToken

from . import views, tests

urlpatterns = [
    path('v1/login/', views.LoginRegister.as_view({'post': 'login'})),
    path('v1/logout/', views.LoginRegister.as_view({'post': 'logout'})),

    path('v2/login/', ObtainJSONWebToken.as_view()),

    path('v1/register/', views.LoginRegister.as_view({'post': 'register'})),
    path('v2/register/', views.LoginRegister2.as_view()),

    path('test/', tests.Test.as_view()),
]
