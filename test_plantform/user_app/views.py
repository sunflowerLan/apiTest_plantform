from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from django.contrib import auth

# Create your views here.

def index(request):

    return render(request, 'user_app/login.html')
    # return HttpResponse('Hello girls.')

def login_action(requset):
    # if requset.method == "GET":
    #     username = requset.GET.get('username')
    #     password = requset.GET.get("password")
    if requset.method == "POST":
        username = requset.POST.get("username", None)
        password = requset.POST.get("password", None)
        # print("username : %s , password : %s" %(username, password))

        # 使用自带的auth_user表结构
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(requset, user)
            return render(requset, "user_app/project_manage.html")
        else:
            error_message = "用户名或密码错误。"
            return render(requset, "user_app/login.html", {"error_message": error_message})

        # 使用定义的user表结构
    #     try:
    #         user = User.objects.get(username_text=username)
    #     except :
    #         error_message = "用户名或密码错误。"
    #         return render(requset, "user_app/login.html", {"error_message": error_message})
    #     if user.password_text == password:
    #         return HttpResponse("欢迎你: %s" % username)

    return render(requset, "user_app/login.html")