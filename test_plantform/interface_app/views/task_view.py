import json
import os
from tkinter import Entry

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from test_plantform.common.common_view import pageInation
from interface_app.models import TestTask, TestCase, TestResult
from interface_app.apps import TASK_PATH, RUN_TASK_FILE
from interface_app.extend.run_task import run_case
from os.path import dirname, abspath
from interface_app.extend.task_thread import TaskThread

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
        task_id = requeset.POST.get("task_id")
        task_name = requeset.POST.get("task_name")
        task_describe = requeset.POST.get("task_describe")
        cases = requeset.POST.get("task_cases")
        if task_name == "":
            return JsonResponse({"success": "false", "message": "任务名称不能为空"})
        if task_id:
            try:
                updatetask = TestTask.objects.get(pk=task_id)
                updatetask.name = task_name
                updatetask.describe = task_describe
                updatetask.cases = cases
                updatetask.save()
                return JsonResponse({"success": "true", "message": "更新成功"})
            except Entry.DoesNotExist:
                return JsonResponse({"success": "false", "message": "更新失败"})
        else:
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
    if request.method == "GET":
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
    if request.method == "GET":
        TestTask.objects.get(pk=task_id).delete()
        return HttpResponseRedirect('/interface/task_manage/')
    else:
        return HttpResponse("404")


def run_task(request, task_id):
    """
    运行测试任务
    :param request:
    :return:
    """
    if request.method == "GET":
        # task_id = request.GET.get("task_id")
        print("进入异步多线程处理。。。")
        TaskThread(task_id).run_thread()
        print("测试任务在单独线程执行中，继续执行后续任务~~~")
        return HttpResponseRedirect("/interface/task_manage/")
    else:
        return HttpResponse("404")


def is_task_run(request):
    """
    如果有任务在执行，返回false；如果没有任务在执行，返回true
    :param request:
    :return: true：
    """
    if request.method == "GET":
        tasks = TestTask.objects.filter(status=1)
        print("当前运行的任务数：", len(tasks))
        if len(tasks) > 0:
            return JsonResponse({"success": "true", "message": "已有任务在运行中，请稍后执行！"})
        else:
            return JsonResponse({"success": "false", "message": "当前没有测试任务运行！"})
    else:
        return JsonResponse({"success": "true", "message": "请求方法有误，请重试！"})