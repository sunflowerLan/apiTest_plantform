from django.test import Client, TestCase
from django.contrib.auth.models import User

# 视图的单元测试
class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('/')
        # print(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_app/login.html')

class LoginActionTest(TestCase):
    def setUp(self):
        User.objects.create_user("test01", "test01@test.mail", "test123")
        self.client = Client()

    # def test_login_null(self):
    #     login_data={"username": "", "password": ""}
    #     response = self.client.post('/login_action/', data=login_data)
    #     login_html = response.content.decode("utf-8")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("用户名或者密码为空", login_html)

    def test_login_error(self):
        login_data = {"username": "abc", "password": "123"}
        response = self.client.post('/login_action/', data=login_data)
        login_html = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("用户名或密码错误", login_html)

    def test_login_success(self):
        login_data = {"username": "test01", "password": "test123"}
        response = self.client.post('/login_action/', data=login_data)
        self.assertEqual(response.status_code, 302)

    def test_login_get(self):
        response = self.client.get('/login_action/')
        self.assertEqual(response.status_code, 200)
        # print(response.content.decode("utf-8"))
        self.assertTemplateUsed(response, 'user_app/login.html')

class LogoutTest(TestCase):
    def setUp(self):
        User.objects.create_user("test01", "test01@mail.com", "test123")
        self.client = Client()
        login_data = {"username": "test01", "password": "test123"}
        self.client.post('/login_action/', data=login_data)

    def test_user_logout(self):
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 302)