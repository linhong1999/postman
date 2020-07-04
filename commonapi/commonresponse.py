# -*- coding: utf-8 -*-
from rest_framework.views import Response
from rest_framework import status as http_status


class CommonResponse(Response):
    class RetConstant:
        MSG = "success"

    def __init__(self,
                 data=None,
                 status=http_status.HTTP_200_OK,
                 message=RetConstant.MSG,
                 result=True,
                 template_name=None,
                 headers=None,
                 exception=False,
                 content_type='application/json'
                 ):

        self.data = {"result": result, "status": status, "message": message, "data": data}
        super().__init__(self.data,
                         status,
                         template_name,
                         headers,
                         exception,
                         content_type)
