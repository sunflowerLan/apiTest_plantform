import re
from django.contrib.auth.decorators import login_required
from django.core.handlers import exception
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from project_app.models import Project
from project_app.models import Module
from interface_app.models import TestCase
import requests
import json

def pageInation(query_obj, default_item, get_page):
    """
    分页功能实现
    :param query_obj:
    :param default_item:
    :param get_page:
    :return:
    """
    # 默认每页显示default_item条
    paginator = Paginator(query_obj, default_item)
    try:
        # 获取第get_page页
        contacts = paginator.page(get_page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    # 返回分页结果
    return contacts

# Create your views here.
@login_required
def case_manage(request):
    """
    测试用例管理
    :param request:
    :return:
    """
    # 读取session
    username = request.session.get('u', None)
    testcase = TestCase.objects.all().order_by('-create_time')
    # 分页
    page = request.GET.get('page')
    contacts = pageInation(testcase, 10, page)
    if request.method == "GET":
        return render(request, 'interface_app/case_manage.html', {'user': username, 'type': 'list', 'testcases': contacts})
    else:
        return HttpResponse("404")

def search_case(request):
    """
    查询测试用例功能实现
    :param request:
    :return:
    """
    if request.method == "POST":
        case_name = request.POST.get("case_name")
        case_module = request.POST.get("case_module")
        # print(case_name, case_module)

        # 判断查询条件是否为空
        if case_name.strip() == "":
            testcase = TestCase.objects.all().order_by('-create_time')
        else:
            testcase = TestCase.objects.filter(Q(name__icontains=case_name)).order_by('-create_time')

        # print("查询结果为：", testcase)
        # 分页
        page = request.GET.get('page')
        contacts = pageInation(testcase, 5, page)
        # 返回查询结果
        return render(request, 'interface_app/case_manage.html',
                          {'type': 'list', 'testcases': contacts, 'case_name': case_name, 'module': case_module})
    else:
        return HttpResponse("404")

def add_case(request):
    """
    打开新增接口页面
    :param request:
    :return:
    """
    if request.method == "GET":
        project_list = Project.objects.all()
        return render(request,'interface_app/case_manage.html', {'type': 'add', 'project_list': project_list})
    else:
        return HttpResponse("404")

@login_required
def debug(request):
    """
    调试接口
    :param request:
    :return:
    """
    # print("request method:" + request.method)
    if request.method == "GET":
        req_url = request.GET.get("url")
        req_method = request.GET.get("method")
        req_parameter = request.GET.get("parameter")
        req_headers = request.GET.get("header")
        req_type = request.GET.get("type")
        # print("url is:"+req_url)
        # print("请求参数:" + req_parameter)
        try:
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
        except json.decoder.JSONDecodeError:
            return HttpResponse("请检查header或参数格式填写是否正确！")
        except BaseException:
            return HttpResponse("调试失败，请检查信息是否正确填写！")
    else:
        return HttpResponse("请求方法错误")


@login_required
def save_case(request):
    """
    保存用例
    :param request:
    :return:
    """
    if request.method == "POST":
        case_id = request.POST.get("case_id")
        req_name = request.POST.get("name")
        req_url = request.POST.get("url")
        req_method = request.POST.get("method")
        req_type = request.POST.get("type")
        req_parameter = request.POST.get("parameter")
        req_headers = request.POST.get("header")
        req_module = request.POST.get("module_id")
        req_assert = request.POST.get("assert")

        if req_url == "" or req_method == "" or req_type == "" or req_module == "":
            return HttpResponse("必传参数为空")
        if req_parameter == "":
            req_parameter = "{}"
        if req_headers == "":
            req_headers = "{}"
        if url_validate(req_url):
            module_obj = Module.objects.get(id=req_module)
            # 如果case_id非空，则更新用例；如果为空，就创建用例
            if case_id:
                # 查找编辑的用例记录
                case = TestCase.objects.get(id=case_id)
                # 获取页面上表单字段更新
                case.name = req_name
                case.module = module_obj
                case.url = req_url
                case.req_method = req_method
                case.req_type = req_type
                case.req_header = req_headers
                case.req_parameter = req_parameter
                case.response_assert = req_assert
                case.save()
                return HttpResponse("更新成功！")
            else:
                testcase = TestCase.objects.create(name=req_name, module=module_obj, url=req_url,
                                           req_method=req_method, req_header=req_headers,
                                           req_type=req_type, req_parameter=req_parameter, response_assert=req_assert)
                if testcase is not None:
                    return HttpResponse("保存成功！")
        else:
            return HttpResponse("请检查URL地址")
    else:
        return HttpResponse("请求方法错误")

@login_required
def edit_case(request, case_id):
    """
    编辑测试用例
    :param request:
    :param case_id:
    :return:
    """
    if request.method == "GET":
        projects = Project.objects.all()
        return render(request, "interface_app/case_manage.html", {'type': 'edit', 'project_list': projects})
    else:
        return HttpResponse("404")

@login_required
def delete_case(request, case_id):
    """
    删除测试用例
    :param request:
    :param case_id:
    :return:
    """
    testcase = TestCase.objects.get(id=case_id)
    testcase.delete()
    return HttpResponseRedirect('/interface/case_manage/')

def url_validate(url):
    """
    验证url地址是否合法
    :param url:
    :return:
    """
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

def get_case_info(request):
    """
    获取测试用例记录
    :param request:
    :return:
    """
    case_id = request.GET.get("case_id")
    # print("case_id", case_id)
    if request.method == "GET":
        if case_id =="":
            return JsonResponse({"success": "false", "message": "case id is Null" })
        case_obj = TestCase.objects.get(pk=case_id)
        # 拿到模块id
        module_id = case_obj.module_id
        # print("模块id：", module_id)

        # 通过模块id找到项目id
        module = Module.objects.get(pk=module_id)
        module_name = module.name

        project_id = module.project_id
        print("项目id：", project_id)

        # 将用例信息返回
        case_info ={
            "name": case_obj.name,
            "url": case_obj.url,
            "req_method": case_obj.req_method,
            "req_header": case_obj.req_header,
            "req_type": case_obj.req_type,
            "req_parameter": case_obj.req_parameter,
            "module_id": module_id,
            "project_id": project_id,
            'response_assert': case_obj.response_assert
        }
        return JsonResponse({"success": "true", "message": "OK", "data": case_info})
    else:
        return HttpResponse("404")

def api_assert(request):
    """
    验证测试用例断言
    :param request:
    :return:
    """
    if request.method == "POST":
        result_text = request.POST.get("result_text")
        assert_text = request.POST.get("assert_text")
        if result_text == "" or assert_text == "":
            return JsonResponse({"success": "false", "message": "验证结果和返回结果不能为空！"})
        try:
            assert assert_text in result_text
        except AssertionError:
            return JsonResponse({"success": "false", "message": "验证失败！"})
        else:
            return JsonResponse({"success": "true", "message": "验证成功！"})
    else:
        return JsonResponse({"success": "false", "message": "请求方法有误！"})

def get_cases_list(request):
    """
    获取测试用例列表
    :param request:
    :return:
    """
    if request.method == 'GET':
        # 项目 -> 模块 -> 用例
        cases_list = []
        projects = Project.objects.all()
        for project in projects:
            modules = Module.objects.filter(project_id=project.id)
            for module in modules:
                cases = TestCase.objects.filter(module_id=module.id)
                for case in cases:
                    # case_dic = {'p_name': project.name, 'm_name': module.name, 'c_name': case.name}
                    case_info = project.name + "->" + module.name + "->" + case.name
                    case_dict = {
                        "id": case.id,
                        "name": case_info
                    }
                    cases_list.append(case_dict)
        return JsonResponse({"success": "true", "message": "请求成功！", "data": cases_list})
    else:
        return JsonResponse({"success": "false", "message": "请求失败！"})