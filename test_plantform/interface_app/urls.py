from django.urls import path, re_path
from interface_app import views

urlpatterns = [
    # 项目
    path('case_manage/', views.case_manage, name='case_manage'),
    path('api_debug/', views.api_debug, name='api_debug'),
    path('debug/', views.debug),
    path('save_case/', views.save_case),
    path('edit_case/<int:case_id>/', views.edit_case, name='edit'),
    path('delete_case/<int:case_id>/', views.delete_case, name='delete'),
    path('search_case/', views.search_case, name="search"),
]