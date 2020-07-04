from django.http import HttpResponse
from django.test import TestCase

# Create your tests here.
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView, Response


class Test(APIView):
    # parser_classes = (FileUploadParser,)
    # def post(self, req, *args, **kwargs):
    #     print(req.data)
    #     print(kwargs)
    #     return Response({
    #         'msg': 'success'
    #     })

    def post(self, req, *args, **kwargs):
        print(req.data)
        return Response({'msg': 'success'})