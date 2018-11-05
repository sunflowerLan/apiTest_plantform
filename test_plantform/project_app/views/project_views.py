from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from project_app.models import Project
from project_app.forms import ProjectForm


# Create your views here.
@login_required
def project_list(request):
    # 读取session
    username = request.session.get('u', None)
    return render(request, 'project_app/project_manage.html', {'user': username, 'type': 'list', 'project_list': Project.objects.all()})

@login_required
def add_project(request):
    # 如果form通过POST方法发送数据
    if request.method == 'POST':
        # 接受request.POST参数构造form类的实例
        form = ProjectForm(request.POST)
        # print(request.POST)
        # 验证数据是否合法
        if form.is_valid():
            name = form.cleaned_data["name"]
            describe = form.cleaned_data["describe"]
            status = form.cleaned_data["status"]
            # create_time = form.cleaned_data["create_time"]
            project = Project(name=name, describe=describe, status=status)
            project.save()
            # return HttpResponse("添加成功")
            return HttpResponseRedirect('/manage/project_manage/')
    # 如果是通过GET方法请求数据，返回一个空的表单
    else:
        form = ProjectForm()
    return render(request, 'project_app/project_manage.html', {'type': 'add', 'form': form})

@login_required
def edit_project(request, project_id):
    # print("编辑项目的id:", project_id)
    if request.method == 'POST':
        # 接受request.POST参数构造form类的实例
        form = ProjectForm(request.POST)
        if form.is_valid():
            # 数据库查询数据
            project = Project.objects.get(id=project_id)
            # 更新数据
            project.name = form.cleaned_data['name']
            project.describe = form.cleaned_data["describe"]
            project.status = form.cleaned_data["status"]
            # 保存
            project.save()
            return HttpResponseRedirect('/manage/project_manage/')
    else:
        project = Project.objects.get(id=project_id)
        form = ProjectForm(instance=project)

    return render(request, "project_app/project_manage.html",{'type': 'edit', 'form': form})

@login_required
def delete_project(request, project_id):
    # 获取参数
    # project_number = request.GET.get()
    # 数据库查找待删除数据
    project = Project.objects.get(id=project_id)
    project.delete()
    return HttpResponseRedirect('/manage/project_manage/')
