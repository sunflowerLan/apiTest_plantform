from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from test_plantform.common.common_view import pageInation
from interface_app.models import TestTask


@login_required
def task_manage(request):
    """
    测试用例管理
    :param request:
    :return:
    """
    # 读取session
    username = request.session.get('u', None)
    testtask = TestTask.objects.all().order_by('-create_time')
    # 分页
    page = request.GET.get('page')
    contacts = pageInation(testtask, 5, page)
    if request.method == "GET":
        return render(request, 'interface_app/task_manage.html', {'user': username, 'type': 'list', 'testtask': contacts})
    else:
        return HttpResponse("404")

def add_task(request):
    """
    打开新增测试任务页面
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, "interface_app/task_manage.html", {'type': 'add'})
    else:
        return HttpResponse("404")

def save_task(requeset):
    """
    保存测试用例
    :param requeset:
    :return:
    """
    if requeset.method == "POST":
        task_name = requeset.POST.get("task_name")
        task_describe = requeset.POST.get("task_describe")
        cases = requeset.POST.get("task_cases")
        if task_name == "":
            return JsonResponse({"success": "false", "message": "任务名称不能为空"})
        task = TestTask.objects.create(name=task_name, describe=task_describe, cases=cases)
        if task is None:
            return JsonResponse({"success": "false", "message": "保存失败"})
        return JsonResponse({"success": "true", "message": "保存成功"})
    else:
        return JsonResponse({"success": "false", "message": "请求错误"})

def edit_task(request, task_id):
    """
    编辑测试任务
    :param request:
    :param task_id:
    :return:
    """
    if request.method =="GET":
        task = TestTask.objects.get(pk=task_id)
        # print(task.name)
        return render(request, "interface_app/task_manage.html", {'type': 'edit', 'task': task})
        pass
    else:
        return HttpResponse("404")

def delete_task(request, task_id):
    """
    删除测试任务
    :param request:
    :param task_id:
    :return:
    """
    if request.method =="GET":
        TestTask.objects.get(pk=task_id).delete()
        return HttpResponseRedirect('/interface/task_manage/')
    else:
        return HttpResponse("404")