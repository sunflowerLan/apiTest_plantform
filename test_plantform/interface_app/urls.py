from django.urls import path, re_path
from interface_app import views

urlpatterns = [
    # 项目
    path('case_manage/', views.case_manage, name='case_manage'),
    path('api_debug/', views.api_debug, name='api_debug'),
    path('debug/', views.debug),
    # path('edit_project/<int:project_id>/', views.edit_project, name='edit'),
    # path('delete_project/<int:project_id>/', views.delete_project, name='delete'),
]