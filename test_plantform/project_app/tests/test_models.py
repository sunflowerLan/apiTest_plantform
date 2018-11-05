from django.test import TestCase
from project_app.models import Project, Module

class ProjectTestCase(TestCase):
    def setUp(self):
        Project.objects.create(name="测试项目01", describe="测试项目描述01", status=1)

    def test_project_create(self):
        Project.objects.create(name="测试项目02", describe="测试项目描述02", status=1)
        Project.objects.create(name="测试项目03", describe="测试项目描述03", status=0)
        project1 = Project.objects.get(name="测试项目02")
        project2 = Project.objects.get(name="测试项目03")
        self.assertEqual(project1.describe, "测试项目描述02")
        self.assertTrue(project1.status)
        self.assertEqual(project2.describe, "测试项目描述03")
        self.assertFalse(project2.status)

    def test_project_update(self):
        project = Project.objects.get(name="测试项目01")
        project.describe = "测试项目描述01_修改"
        project.status = 0
        project.save()
        project_after = Project.objects.get(name="测试项目01")
        self.assertEqual(project_after.describe, "测试项目描述01_修改")
        self.assertFalse(project_after.status)

    def test_project_query(self):
        project = Project.objects.get(name="测试项目01")
        self.assertEqual(project.describe, "测试项目描述01")
        self.assertTrue(project.status)

    def test_project_delete(self):
        project = Project.objects.get(name="测试项目01")
        project.delete()
        project_delete = Project.objects.filter(name="测试项目01")
        self.assertEqual(len(project_delete), 0)

class ModuleTestCase(TestCase):
    def setUp(self):
        project = Project.objects.create(name="测试项目01", describe="测试项目描述01", status=1)
        Module.objects.create(name="测试模块01", describe="测试模块描述01", project=project)

    def test_module_create(self):
        project = Project.objects.get(name="测试项目01")
        Module.objects.create(name="测试模块02", describe="测试模块描述02", project=project)
        module = Module.objects.get(name="测试模块02")
        self.assertEqual(module.describe, "测试模块描述02")
        self.assertEqual(module.project, project)

    def test_module_query(self):
        module = Module.objects.get(name="测试模块01")
        self.assertEqual(module.describe, "测试模块描述01")

    def test_module_update(self):
        project = Project.objects.create(name="测试项目02", describe="测试项目描述02", status=1)
        module = Module.objects.get(name="测试模块01")
        module.describe ="测试模块描述01_修改"
        module.project = project
        module.save()
        module_after = Module.objects.get(name="测试模块01")
        self.assertEqual(module_after.describe, "测试模块描述01_修改")
        self.assertEqual(module_after.project, project)

    def test_module_delete(self):
        module = Module.objects.get(name="测试模块01")
        module.delete()
        module_after = Module.objects.filter(name="测试模块01")
        self.assertEqual(len(module_after), 0)

    def test_delete_project_and_module(self):
        project = Project.objects.get(name="测试项目01")
        project.delete()
        module = Module.objects.filter(name="测试模块01")
        self.assertEqual(len(module), 0)
