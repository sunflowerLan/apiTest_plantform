from django.shortcuts import render
from django.http import HttpResponse
from .models import Project


# Create your views here.

def add_action(request):
    return render(request, "project_app/project_add.html")


def save_action(request):
    project_number = request.POST.get("projectID", None)
    project_name = request.POST.get("projectName", None)
    begin_date = request.POST.get("beginDate", None)
    project_manager = request.POST.get("projectManager", None)
    project_des = request.POST.get("projectDes", None)
    project = Project(projectNumber_text=project_number, projectName_text=project_name, startDate=begin_date,
                      projectManager_text=project_manager, projectDes_text=project_des)
    project.save()
    # return HttpResponse("添加成功")
    return render(request, "user_app/project_manage.html", {'project_list': find_project_list()})


def find_project_list():
    project_list = Project.objects.all()
    return project_list

def find_project_by_projectId(project_id):
    project = Project.objects.get(projectNumber_text=project_id)
    return project

def open_editpage(request, project_id):
    return render(request, "project_app/project_edit.html", {'project': find_project_by_projectId(project_id)})

def update_action(request,project_id):
    # 数据库查询数据
    project = Project.objects.get(projectNumber_text=project_id)
    # 更新数据
    project.projectName_text = request.POST.get("projectName", None)
    project.projectManager_text = request.POST.get("projectManager", None)
    project.projectDes_text = request.POST.get("projectDes", None)
    project.startDate = request.POST.get("beginDate", None)
    # 保存
    project.save()
    return render(request, "user_app/project_manage.html", {'project_list': find_project_list()})


def delete_action(request, project_id):
    # 获取参数
    # project_number = request.GET.get()
    # 数据库查找待删除数据
    project = Project.objects.get(projectNumber_text=project_id)
    project.delete()
    return render(request, "user_app/project_manage.html", {'project_list': find_project_list()})
