from django.contrib.auth.models import User
from django.test import TestCase
from project_app.models import Module, Project

class ModuleManageTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        project = Project.objects.create(name="测试项目01", describe="测试项目01描述", status=True)
        Module.objects.create(project=project, name="测试模块01", describe="测试模块01描述")
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_module_manage(self):
        """项目管理"""
        response = self.client.get('/manage/module_manage/')
        project_html = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn("模块列表", project_html)

class ModuleAddTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        project = Project.objects.create(name="测试项目01", describe="测试项目01描述")
        Module.objects.create(project=project, name="测试模块01", describe="测试模块01描述")
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_module_add_get(self):
        response = self.client.get('/manage/add_module/')
        module_html = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn("新增模块", module_html)

    def test_module_add_invalid(self):
        project = Project.objects.get(name="测试项目01")
        module_form = {"project": project.id, "name": "", "describe": ""}
        response = self.client.post('/manage/add_module/', data=module_form)
        module_html = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn("新增模块", module_html)

    def test_module_add_success(self):
        project = Project.objects.get(name="测试项目01")
        module_form = {"project": project.id, "name": "新增测试模块01", "describe": "新增测试模块描述01"}
        response = self.client.post('/manage/add_module/', data=module_form)
        # module_html = response.content.decode('utf-8')
        # print(module_html)
        self.assertEqual(response.status_code, 302)

class ModuleEditTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        project = Project.objects.create(name="测试项目01", describe="测试项目01描述")
        Module.objects.create(project=project, name="测试模块01", describe="测试模块01描述")
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_module_edit_get(self):
        # project = Project.objects.get(name="测试项目01")
        module = Module.objects.get(name="测试模块01")
        response = self.client.get('/manage/edit_module/%d/' % module.id)
        module_html = response.content.decode('utf-8')
        # print(project_html)
        self.assertEqual(response.status_code, 200)
        self.assertIn("编辑模块", module_html)

    def test_module_edit_invalid(self):
        project = Project.objects.get(name="测试项目01")
        module = Module.objects.get(name="测试模块01")
        update_data = {"project": project.id, "name": "", "describe": ""}
        response = self.client.post('/manage/edit_module/%d/' % module.id, data=update_data)
        module_html = response.content.decode('utf-8')
        # print(project_html)
        self.assertEqual(response.status_code, 200)
        self.assertIn("编辑模块", module_html)

    def test_module_edit_success(self):
        project = Project.objects.get(name="测试项目01")
        module = Module.objects.get(name="测试模块01")
        update_data = {"project": project.id, "name": "编辑测试模块01", "describe": "编辑测试模块描述01"}
        response = self.client.post('/manage/edit_module/%d/' % module.id, data=update_data)
        response.content.decode('utf-8')
        self.assertEqual(response.status_code, 302)

class ModuleDeleteTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        project = Project.objects.create(name="测试项目01", describe="测试项目01描述")
        Module.objects.create(project=project, name="测试模块01", describe="测试模块01描述")
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_module_delete_success(self):
        module = Module.objects.get(name="测试模块01")
        response = self.client.get('/manage/delete_module/%d/' % module.id)
        response.content.decode('utf-8')
        self.assertEqual(response.status_code, 302)