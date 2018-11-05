from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.

# 模型的单元测试
class UserTestCase(TestCase):

    def setUp(self):
        User.objects.create_user("test01", "test01@mail.com", "test123456")

    def test_user_create(self):
        User.objects.create_user("test02", "test02@mail.com", "test123456")
        user = User.objects.get(username="test02")
        self.assertEqual(user.email, "test02@mail.com")

    def test_user_query(self):
        user = User.objects.get(username="test01")
        self.assertEqual(user.email, "test01@mail.com")

    def test_user_update(self):
        user = User.objects.get(username="test01")
        user.email = "test001@mail.com"
        user.username = "test001"
        user.save()
        update_user = User.objects.get(username="test001")
        self.assertEqual(user.email, "test001@mail.com")

    def test_user_delete(self):
        user = User.objects.get(username="test01")
        user.delete()
        delete_user = User.objects.filter(username="test01")
        # print(delete_user)
        self.assertEqual(len(delete_user), 0)
