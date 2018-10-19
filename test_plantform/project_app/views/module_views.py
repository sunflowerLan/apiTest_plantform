from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from project_app.models import Module
from project_app.forms import ModuleForm

# Create your views here.
@login_required
def module_manage(request):
    # 读取session
    username = request.session.get('u', None)
    return render(request, 'project_app/module_manage.html', {'user': username, 'type': 'list', 'module_list': Module.objects.all()})

@login_required
def add_module(request):
    # 如果form通过POST方法发送数据
    if request.method == 'POST':
        # 接受request.POST参数构造form类的实例
        form = ModuleForm(request.POST)
        # 验证数据是否合法
        if form.is_valid():
            name = form.cleaned_data["name"]
            describe = form.cleaned_data["describe"]
            # create_time = form.cleaned_data["create_time"]
            project = form.cleaned_data["project"]
            module = Module(name=name, describe=describe, project=project)
            module.save()
            return HttpResponseRedirect('/manage/module_manage/')
    # 如果是通过GET方法请求数据，返回一个空的表单
    else:
        form = ModuleForm()
    return render(request, 'project_app/module_manage.html', {'type': 'add', 'form': form})

@login_required
def edit_module(request, module_id):
    # print("编辑项目的id:", project_id)
    if request.method == 'POST':
        # 接受request.POST参数构造form类的实例
        form = ModuleForm(request.POST)
        if form.is_valid():
            # 数据库查询数据
            module = Module.objects.get(id=module_id)
            # 更新数据
            module.name = form.cleaned_data['name']
            module.describe = form.cleaned_data["describe"]
            module.project = form.cleaned_data["project"]
            # 保存
            module.save()
            return HttpResponseRedirect('/manage/module_manage/')
    else:
        if module_id:
            module = Module.objects.get(id=module_id)
            form = ModuleForm(instance=module)
        return render(request, "project_app/module_manage.html",{'type': 'edit', 'form': form})

@login_required
def delete_module(request, module_id):
    # 获取参数
    # project_number = request.GET.get()
    # 数据库查找待删除数据
    module = Module.objects.get(id=module_id)
    module.delete()
    return HttpResponseRedirect('/manage/module_manage/')
