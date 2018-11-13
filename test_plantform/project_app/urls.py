from django.urls import path
from project_app.views import project_views, module_views

urlpatterns = [
    # 项目
    path('project_manage/', project_views.project_list, name='project_list'),
    path('add_project/', project_views.add_project, name='add_project'),
    path('edit_project/<int:project_id>/', project_views.edit_project, name='edit'),
    path('delete_project/<int:project_id>/', project_views.delete_project, name='delete'),

    # 模块
    path('module_manage/', module_views.module_manage),
    path('add_module/', module_views.add_module_action),
    path('edit_module/<int:module_id>/', module_views.edit_module),
    path('delete_module/<int:module_id>/', module_views.delete_module),

    # 通过项目查找所有关联的模块
    path('find_modules_of_project/', module_views.find_modules_of_project)
]