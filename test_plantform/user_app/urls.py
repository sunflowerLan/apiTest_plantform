from django.conf.urls import url
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login_action/', views.login_action, name='login'),
    path('logout/', views.logout, name='logout')
]