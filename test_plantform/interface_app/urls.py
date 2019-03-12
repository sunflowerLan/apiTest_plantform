from django.urls import path, re_path
from .views import case_view, task_view, result_view

urlpatterns = [
    # 测试用例
    path('case_manage/', case_view.case_manage, name='case_manage'),
    path('add_case/', case_view.add_case, name='api_debug'),
    path('api_debug/', case_view.debug),
    path('save_case/', case_view.save_case),
    path('edit_case/<int:case_id>/', case_view.edit_case, name='edit'),
    path('delete_case/<int:case_id>/', case_view.delete_case, name='delete'),
    path('search_case/', case_view.search_case, name="search"),
    path('get_case_info/', case_view.get_case_info, name="getCaseInfo"),
    path('api_assert/', case_view.api_assert),
    path('get_cases_list/', case_view.get_cases_list),

    #测试计划
    path('task_manage/', task_view.task_manage),
    path('add_task/', task_view.add_task),
    path('save_task/', task_view.save_task),
    path('run_task/<int:task_id>/', task_view.run_task),
    path('edit_task/<int:task_id>/', task_view.edit_task),
    path('delete_task/<int:task_id>/', task_view.delete_task),
    path('is_task_run/', task_view.is_task_run),

    # 测试结果
    path('task_result_list/<int:task_id>/', result_view.task_result_list),
    path('result_detail/', result_view.result_detail),
]