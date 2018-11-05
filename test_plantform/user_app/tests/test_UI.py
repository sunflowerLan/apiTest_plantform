from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver import Chrome

class LoginTests(StaticLiveServerTestCase):
    # fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = Chrome()
        cls.driver.implicitly_wait(10)

    def setUp(self):
        User.objects.create_user("test01", "test01@mail.com", "test123")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_login(self):
        self.driver.get('%s%s' % (self.live_server_url, '/login_action/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('test01')
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('test123')
        self.driver.find_element_by_id('loginButton').click()