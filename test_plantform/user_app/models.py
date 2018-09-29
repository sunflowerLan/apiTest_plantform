from django.db import models
from django.conf import settings

# Create your models here.

# 自定义的user模型
# class User(models.Model):
#     username_text = models.CharField(max_length=50, unique=True)
#     password_text = models.CharField(max_length=50)
#     def __str__(self):
#         return self.username_text

# Django自带auth模块的User用户表，如果你想在自己的项目里创建用户模型，又想方便的使用Django的认证功能，
# 那么一个比较好的方案就是在你的用户模型里，使用一对一关系，添加一个与auth模块User模型的关联字段
class MySpecialUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    supervisor = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='supervisor_of',
    )