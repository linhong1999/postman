# -*- coding: utf-8 -*-
from rest_framework.views import Response


class MyResponse(Response):
    def __init__(self, data_status=0, data_msg='ok', result=None, http_status=None, headers=None, exception=False):
        data = {
            'status': data_status,
            'msg': data_msg,
            'result': result
        }

        super().__init__(data=data, status=http_status, headers=headers, exception=exception)