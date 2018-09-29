### 主流程

1. 安装python3.6、django2.1
~~~
pip install django==2.1
~~~
2. 创建项目
~~~
django-admin startproject test_platform
~~~
3. 创建APP
~~~
python manage.py startapp user_app
~~~
4. 打开test_platform/settings 注册APP
~~~
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_app',
]
~~~
5. 认识django MTV 模式
  * M 代表模型(Model),即数据存取层。 该层处理与数据相关的所有事务： 如何存取、 如何验证有效
  * T 代表模板(Template),即表现层。 该层处理与表现相关的决定： 如何在页面或其他类型文档中进行显示。
  * V 代表视图(View),即业务逻辑层。

6. 在test_platform/urls 下面添加路由，在APP下面新建templates，存放html文件，views编写逻辑
7. 未使用models.py ，实现假登录业务

8. 启动项目
~~~
python manage.py runserver
~~~

