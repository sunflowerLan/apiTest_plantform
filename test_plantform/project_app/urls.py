from django.urls import path
from . import views

urlpatterns = [
    # path('newProject/', views.create, name='open_newpage'),
    path('add/', views.add_action, name='project_add'),
    path('save/', views.save_action, name='project_save'),
    path(r'edit/<int:project_id>', views.open_editpage, name='project_edit'),
    path(r'update/<int:project_id>', views.update_action, name='project_update'),
    path(r'delete/<int:project_id>', views.delete_action, name='project_delete'),
]