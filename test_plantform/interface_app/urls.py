from django.urls import path, re_path
from interface_app import views

urlpatterns = [
    # 项目
    path('case_manage/', views.case_manage, name='case_manage'),
    path('add_case/', views.add_case, name='api_debug'),
    path('api_debug/', views.debug),
    path('save_case/', views.save_case),
    path('edit_case/<int:case_id>/', views.edit_case, name='edit'),
    path('delete_case/<int:case_id>/', views.delete_case, name='delete'),
    path('search_case/', views.search_case, name="search"),
    path('get_case_info/', views.get_case_info, name="getCaseInfo"),
    path('api_assert/', views.api_assert),
]