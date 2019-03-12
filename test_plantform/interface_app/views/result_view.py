from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from interface_app.models import TestResult, TestTask


def task_result_list(request, task_id):
    """
    获取测试任务的运行结果
    :param request:
    :param task_id:
    :return:
    """
    if request.method == "GET":
        task = TestTask.objects.get(id=task_id)
        test_results = TestResult.objects.filter(task_id=task_id)
        return render(request, 'interface_app/task_manage.html',
                      {'type': 'result', 'task_result_list': test_results, 'task_name': task.name})
    else:
        return HttpResponse("404")


def result_detail(request):
    """
    查询测试结果
    :param request:
    :param result_id:
    :return:
    """
    if request.method == "GET":
        result_id = request.GET.get("result_id")
        # print("result_id: ", result_id)
        try:
            test_result = TestResult.objects.get(id=result_id)
            # print(test_result.result)
            return JsonResponse({"success": "true", "message": "", "data": test_result.result})
        except BaseException:
            return JsonResponse({"success": "false", "message": "查询结果失败"})
    else:
        return JsonResponse({"success": "false", "message": "请求方法错误!"})