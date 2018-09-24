from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login_action/', views.login_action, name='login')
]