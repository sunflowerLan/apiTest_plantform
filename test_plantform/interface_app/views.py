import re
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from project_app.models import Project
from project_app.models import Module
from .models import TestCase
from .forms import TestCaseForm
import requests
import json

# Create your views here.
@login_required
def case_manage(request):
    # 读取session
    username = request.session.get('u', None)
    testcase = TestCase.objects.all()
    # 分页
    paginator = Paginator(testcase, 3)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)

    if request.method == "GET":
        return render(request, 'interface_app/case_manage.html', {'user': username, 'type': 'list', 'testcases': contacts})
    else:
        return HttpResponse("404")

# 查询
def search_case(request):
    if request.method == "POST":
        case_name = request.POST.get("case_name")
        case_module = request.POST.get("case_module")
        # print(case_name, case_module)

        # 判断查询条件是否为空
        if case_name.strip() == "":
            testcase = TestCase.objects.all()
        else:
            testcase = TestCase.objects.filter(Q(name__icontains=case_name))

        # 分页
        paginator = Paginator(testcase, 3)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
            return render(request, 'interface_app/case_manage.html',
                          {'type': 'list', 'testcases': contacts, 'case_name': case_name, 'module': case_module})
    else:
        return HttpResponse("404")

# 进入调试接口页面
def api_debug(request):
    if request.method == "GET":
        project_list = Project.objects.all()
        return render(request,'interface_app/case_manage.html', {'type': 'debug', 'project_list': project_list})
    else:
        return HttpResponse("404")

# 调试接口
@login_required
def debug(request):
    # print("request method:" + request.method)
    if request.method == "GET":
        req_url = request.GET.get("url")
        req_method = request.GET.get("method")
        req_parameter = request.GET.get("parameter")
        req_headers = request.GET.get("header")
        req_type = request.GET.get("type")
        # print("url is:"+req_url)
        # print("请求参数:" + req_parameter)
        # 判断url地址
        if url_validate(req_url):
            if req_method.upper() == "GET":   # get请求
                r = requests.get(req_url, params=json.loads(req_parameter), headers=json.loads(req_headers))
            elif req_method.upper() == "POST":  # post请求
                if req_type == "form-data":
                    r = requests.post(req_url, data=json.loads(req_parameter), headers=json.loads(req_headers))
                else:
                    r = requests.post(req_url, json=req_parameter, headers=json.loads(req_headers))
            elif req_method.upper() == "PUT":
                r = requests.put(req_url, data=json.loads(req_parameter))
            elif req_method.upper() == "DELETE":
                r = requests.delete(req_url)
            elif req_method.upper() == "HEAD":
                r = requests.head(req_url)
            elif req_method.upper() == "OPTION":
                r = requests.options(req_url)
            # print(r.status_code)
            # print(r.text)
            return HttpResponse(json.dumps(r.text))
        else:
            return HttpResponse("请检查URL地址")
    else:
        return HttpResponse("请求方法错误")

# 保存用例
@login_required
def save_case(request):
    if request.method == "POST":
        req_name = request.POST.get("name")
        req_url = request.POST.get("url")
        req_method = request.POST.get("method")
        req_type = request.POST.get("type")
        req_parameter = request.POST.get("parameter")
        req_headers = request.POST.get("header")
        req_module = request.POST.get("module_id")

        if req_url == "" or req_method == "" or req_type == "" or req_module == "":
            return HttpResponse("必传参数为空")
        if req_parameter == "":
            req_parameter = "{}"
        if req_headers == "":
            req_headers = "{}"
        if url_validate(req_url):
            module_obj = Module.objects.get(id=req_module)
            # print(module_obj)
            testcase = TestCase.objects.create(name=req_name, module=module_obj, url=req_url,
                                       req_method=req_method, req_header=req_headers,
                                       req_type=req_type, req_parameter=req_parameter)
            if testcase is not None:
                return HttpResponse("保存成功！")
        else:
            return HttpResponse("请检查URL地址")
    else:
        return HttpResponse("请求方法错误")

# 编辑测试用例
@login_required
def edit_case(request, case_id):
    # print("编辑测试用例id：%d" %case_id)
    # print("测试方法："+ request.method)
    if request.method == "POST":
        form = TestCaseForm(request.POST)
        if form.is_valid():
            # 查找编辑的用例记录
            case = TestCase.objects.get(id=case_id)
            # 获取页面上表单字段
            case.name = form.cleaned_data['name']
            case.module = form.cleaned_data['module']
            case.url = form.cleaned_data['url']
            case.req_method = form.cleaned_data['req_method']
            case.req_type = form.cleaned_data['req_type']
            case.req_header = form.cleaned_data['req_header']
            case.req_parameter = form.cleaned_data['req_parameter']
            case.response_assert = form.cleaned_data['response_assert']
            # 获取参数进行判断
            if case.url == "" or case.req_method == "" or case.req_type == "" or case.module == "":
                return HttpResponse("必传参数为空")
            if case.req_parameter == "":
                case.req_parameter = "{}"
            if case.req_header == "":
                case.req_header = "{}"
            case.save()
            return HttpResponseRedirect('/interface/case_manage/')
    else:
        testcase = TestCase.objects.get(id=case_id)
        form = TestCaseForm(instance=testcase)
    return render(request, "interface_app/case_manage.html", {'type': 'edit', 'form': form})

# 删除测试用例
@login_required
def delete_case(request, case_id):
    testcase = TestCase.objects.get(id=case_id)
    testcase.delete()
    return HttpResponseRedirect('/interface/case_manage/')

# 验证url地址是否合法
def url_validate(url):
    flag = False
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if re.match(regex, url):
        flag = True
    return flag