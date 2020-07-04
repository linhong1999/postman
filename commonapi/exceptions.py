# -*- coding: utf-8 -*-
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import exception_handler as handler

from .commonresponse import CommonResponse

def exception_handler(exc, context):

    response = handler(exc,context)

    if response is None:
        print('%s - %s - %s ' % (context['view'], context['request'].method, exc))
        return CommonResponse(
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            result=False, message='server error', exception=True)
