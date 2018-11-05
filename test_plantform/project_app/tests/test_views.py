from django.contrib.auth.models import User
from project_app.models import Project
from django.test import TestCase, Client

# Create your tests here.


class ProjectManageTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Project.objects.create(name="xx项目", describe="xx描述")
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_project_manage(self):
        """项目管理"""
        response = self.client.get('/manage/project_manage/')
        project_html = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        # self.assertIn("测试平台项目测试", project_html)

class ProjectAddTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Project.objects.create(name="xx项目", describe="xx描述")
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_project_add_get(self):
        response = self.client.get('/manage/add_project/')
        project_html = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn("新增项目", project_html)

    def test_project_add_invalid(self):
        project_form = {"name": "", "describe": "", "status": True }
        response = self.client.post('/manage/add_project/', data=project_form)
        project_html = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn("新增项目", project_html)

    def test_project_add_success(self):
        data = {"name": "新增测试项目01", "describe": "新增测试项目描述01", "status": True}
        response = self.client.post('/manage/add_project/', data=data)
        project_html = response.content.decode('utf-8')
        # print(project_html)
        self.assertEqual(response.status_code, 302)

class ProjectEditTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Project.objects.create(name="新增测试项目01", describe="新增测试项目01描述")
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_project_edit_get(self):
        project = Project.objects.get(name="新增测试项目01")
        # update_data = {"name": "编辑测试项目01", "describe": "编辑测试项目描述01", "status": False}
        response = self.client.get('/manage/edit_project/%d/' % project.id)
        project_html = response.content.decode('utf-8')
        # print(project_html)
        self.assertEqual(response.status_code, 200)
        self.assertIn("编辑项目", project_html)

    def test_project_edit_invalid(self):
        project = Project.objects.get(name="新增测试项目01")
        update_data = {"name": "", "describe": ""}
        response = self.client.post('/manage/edit_project/%d/' % project.id, data=update_data)
        project_html = response.content.decode('utf-8')
        # print(project_html)
        self.assertEqual(response.status_code, 200)
        self.assertIn("编辑项目", project_html)

    def test_project_edit_success(self):
        project = Project.objects.get(name="新增测试项目01")
        update_data = {"name": "编辑测试项目01", "describe": "编辑测试项目描述01", "status": False}
        response = self.client.post('/manage/edit_project/%d/' % project.id, data=update_data)
        response.content.decode('utf-8')
        self.assertEqual(response.status_code, 302)

class ProjectDeleteTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Project.objects.create(name="新增测试项目01", describe="新增测试项目01描述")
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_project_delete_success(self):
        project = Project.objects.get(name="新增测试项目01")
        response = self.client.get('/manage/delete_project/%d/' % project.id)
        response.content.decode('utf-8')
        self.assertEqual(response.status_code, 302)