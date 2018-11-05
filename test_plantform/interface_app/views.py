import re

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
import requests
import json

# Create your views here.
@login_required
def case_manage(request):
    # 读取session
    username = request.session.get('u', None)
    return render(request, 'interface_app/case_manage.html', {'user': username, 'type': 'list'})

# 创建接口
def api_debug(request):
    if request.method == "GET":
        return render(request,'interface_app/case_manage.html', {'type': 'debug'})
    else:
        return HttpResponse("404")

@login_required
def debug(request):
    req_name = request.POST.get("name")
    req_url = request.POST.get("url")
    req_method = request.POST.get("method")
    req_parameter = request.POST.get("parameter")
    req_headers = request.POST.get("header")
    # print("url is:"+req_url)
    # print("请求参数:" + req_parameter)
    # print(req_parameter)
    # 判断url地址
    if url_validate(req_url):
        if req_method.upper() == "GET":   # get请求
            r = requests.get(req_url, params=json.loads(req_parameter), headers=json.loads(req_headers))
        elif req_method.upper() == "POST":  # post请求
            r = requests.post(req_url, data=json.loads(req_parameter), headers=json.loads(req_headers))
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