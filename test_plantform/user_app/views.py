from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):

    return render(request, 'user_app/login.html')
    # return HttpResponse('Hello girls.')

def login_action(requset):
    if requset.method == "GET":
        username = requset.GET.get('username')
        password = requset.GET.get("password")

        if username == "" or password == "":
            error_message = "用户名和密码不能为空。"
            return render(requset, "user_app/login.html", {"error_message": error_message})
            # return HttpResponse("用户名或密码为空")