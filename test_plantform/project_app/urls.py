from django.urls import path
from . import views

urlpatterns = [
    path('project_manage/', views.project_list, name='project_list'),
    path('add_project/', views.add_project, name='add_project'),
    path('edit_project/<int:project_id>/', views.edit_project, name='edit'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete'),
]