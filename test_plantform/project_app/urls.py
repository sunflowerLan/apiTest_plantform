from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_action, name='project_add'),
    path('update/', views.update_action, name='project_add'),
    path('delete/', views.delete_action, name='project_delete'),
]