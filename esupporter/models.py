from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):
    username = models.CharField(_('username'), max_length=150, blank=True)
    name = models.CharField(max_length=255, null=True, unique=False)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# 要約用の質問＆回答のテーブル
class Question(models.Model):
    user_id = models.IntegerField()
    question = models.CharField(max_length=100)
    answer = models.TextField(blank=True, null=True, max_length=1000)

# ES保存用の会社テーブル
class Company(models.Model):
    user_id = models.IntegerField()
    company_name = models.CharField(max_length=100)


# 会社へのエントリーシートに使用した質問＆回答のテーブル
class ES(models.Model):
    user_id = models.IntegerField()
    company_id  = models.IntegerField()
    question = models.CharField(max_length=100)
    answer = models.TextField(blank=True, null=True, max_length=1000)

