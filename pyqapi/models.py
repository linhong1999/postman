from django.db import models
from userapi import models as user_api_model


class BaseModel(models.Model):
    is_delete = models.BooleanField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Pyq(BaseModel):
    user = models.ForeignKey(user_api_model.User, on_delete=models.CASCADE)
    content = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = 'pyq'

    # def __str__(self):
    #     return '用户 %s 发表了一条 %s' % (self.user.username, self.content)

    def username(self):
        return self.user.username

    def user_img(self):
        return str(self.user.img)

    # @property
    # def comments(self):
    #     return Comment.objects


class Comment(BaseModel):
    user = models.ForeignKey(user_api_model.User, on_delete=models.DO_NOTHING)
    pyq_obj = models.ForeignKey(Pyq, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)

    @property
    def username(self):
        return self.user.username

    @property
    def user_img(self):
        return str(self.user.img)

    class Meta:
        db_table = 'comment'

    def __str__(self):
        return self.comment
        # return '用户 %s 评论了 %s 的 朋友圈: %s ,评论的内容是 %s' % \
        #        (self.user.username, self.pyq_obj.user.username, self.pyq_obj.id, self.comment)


class Wink(BaseModel):
    user = models.ForeignKey(user_api_model.User, on_delete=models.DO_NOTHING)
    pyq_obj = models.ForeignKey(Pyq, on_delete=models.CASCADE)

    def __str__(self):
        return '%s 点赞了 %s' % (self.user.username,self.pyq_obj.id)

    class Meta:
        db_table = 'wink'

    def username(self):
        return self.user.username