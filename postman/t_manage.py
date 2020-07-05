# -*- coding: utf-8 -*-

import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'postman.settings')
django.setup()

#
# os.environ.setdefault('token','ssssssssssss')
# print(os.environ.get('token'))

#

# obj = models.Wink.objects.filter(pyq_obj_id=1, user_id=3).first()
# obj.is_delete = not obj.is_delete
# obj.save()
# models.Wink(
#     user_id=2,pyq_obj_id=1
# ).save()

# query = models.Pyq.objects.filter(is_delete=False)
# date_set = set()
# souted_query_dict = dict()
# for obj in query:
#     date_set.add((obj.create_time.year,obj.create_time.month,obj.create_time.day))
#     souted_query_dict = {}.fromkeys(date_set,[])
#     souted_query_dict[(obj.create_time.year,obj.create_time.month,obj.create_time.day)].append(obj)
# print(souted_query_dict)
# print(models.Pyq.objects.get(pk=1).comment_set.only('comment'))
# obj = models.Pyq.objects.only('is_delete')
# print(obj.first().content)
# print(models.Pyq.objects.all())
