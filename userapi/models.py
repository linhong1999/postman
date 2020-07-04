from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    SEX_CHOICES = [
        [0, 'male'],
        [1, 'female']
    ]
    sex = models.IntegerField(
        choices=SEX_CHOICES,
        default=0,
        error_messages={
            'choices': _("You must choose male or female"),
        },
    )
    # img = models.ImageField(upload_to='img', default='img/default.png')
    img = models.FileField(upload_to='img', default='img/default.png')

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)
    #
    def set_password(self, raw_password):
        super(User, self).set_password(raw_password)

    # def check_password(self, raw_password):
    #     super(User, self).check_password(raw_password)

    @property
    def get_sex(self):
        return self.get_sex_display()

    class Meta:
        db_table = 'user'
        verbose_name = '自定义用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class TestUser(models.Model):
    SEX_CHOICES = [
        [0, 'male'],
        [1, 'female']
    ]
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    sex = models.IntegerField(
        choices=SEX_CHOICES,
        default=0,
        error_messages={
            'choices': _("You must choose male or female"),
        },
    )
    icon = models.ImageField(upload_to='icon', default='icon/default.jpeg')

    @property
    def get_sex(self):
        return self.get_sex_display()

    class Meta:
        db_table = 'testuser'
        verbose_name = '测试用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
