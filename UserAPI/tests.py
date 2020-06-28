from django.test import TestCase

# Create your tests here.
from rest_framework.views import APIView, Response


class Test(APIView):

    def post(self, req, *args, **kwargs):
        print(req.data)
        print(kwargs)
        return Response({
            'msg': 'success'
        })