import time
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver import Chrome

from project_app.models import Project
from selenium.webdriver.support.select import Select


class ProjectTests(StaticLiveServerTestCase):
    # fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = Chrome()
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def setUp(self):
        self.login_action()

    def login_action(self):
        User.objects.create_user("test01", "test01@mail.com", "test123")
        self.driver.get('%s%s' % (self.live_server_url, '/login_action/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('test01')
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('test123')
        self.driver.find_element_by_id('loginButton').click()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_project_manage(self):
        self.driver.get('%s%s' %(self.live_server_url, '/manage/project_manage/'))
        time.sleep(3)
        login_user = self.driver.find_element_by_id('loginUser').text
        # print(login_user)
        self.assertIn("test01", login_user)

    def test_project_add(self):
        self.driver.get('%s%s' % (self.live_server_url, '/manage/project_manage/'))
        self.driver.find_element_by_id('add_project').click()
        time.sleep(3)
        name = self.driver.find_element_by_name("name")
        describe = self.driver.find_element_by_name("describe")
        name.send_keys("新增测试项目")
        describe.send_keys("项目描述")
        self.driver.find_element_by_id("save_project").click()

class ModuleTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = Chrome()
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        Project.objects.create(name="测试项目01", describe="项目描述")
        User.objects.create_user("test01", "test01@mail.com", "test123")
        self.driver.get('%s%s' % (self.live_server_url, '/login_action/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('test01')
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('test123')
        self.driver.find_element_by_id('loginButton').click()

    def tearDown(self):
        pass

    def test_module_manage(self):
        self.driver.get('%s%s' % (self.live_server_url, '/manage/module_manage/'))
        time.sleep(3)
        login_user = self.driver.find_element_by_id('module_list').text
        # print(login_user)
        self.assertEqual("模块列表", login_user)

    def test_module_add(self):
        self.driver.get('%s%s' % (self.live_server_url, '/manage/module_manage/'))
        self.driver.find_element_by_id('add_module').click()
        time.sleep(3)
        project = Select(self.driver.find_element_by_name("project"))
        project.select_by_visible_text("测试项目01")
        name = self.driver.find_element_by_name("name")
        describe = self.driver.find_element_by_name("describe")
        name.send_keys("新增测试模块")
        describe.send_keys("模块描述")
        self.driver.find_element_by_id("save_module").click()
