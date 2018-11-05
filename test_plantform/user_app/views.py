from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
# Create your views here.
from django.urls import reverse

def index(request):

    return render(request, 'user_app/login.html')
    # return HttpResponse('Hello girls.')

def login_action(request):

    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        # print("username : %s , password : %s" % (username, password))

        # 使用自带的auth_user表结构
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # 记录用户的登录状态
            auth.login(request, user)
            # 使用session
            # request.session.set_expiry(3600)
            # request.session['is_login'] = True
            request.session['u'] = user.username

            # 使用cookie
            # response.set_cookie('u', user, expires=3600)
            return HttpResponseRedirect('/manage/project_manage/')  # 页面跳转
        else:
            error_message = "用户名或密码错误"
            return render(request, "user_app/login.html", {"error_message": error_message})

        # 使用定义的user表结构
    #     try:
    #         user = User.objects.get(username_text=username)
    #     except :
    #         error_message = "用户名或密码错误。"
    #         return render(requset, "user_app/login.html", {"error_message": error_message})
    #     if user.password_text == password:
    #         return HttpResponse("欢迎你: %s" % username)

    return render(request, "user_app/login.html")

# @login_required #判断用户是否登录
# def project_manage(request):
#     # username = request.COOKIES.get('u',None) #读取cookie
#     username = request.session.get('u', None) #读取session
#     project_all = project_app.views.find_project_list()
#     return render(request, "project_app/project_manage.html", {'user': username, 'project_list': project_all})
@login_required
def logout(request):
    # request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['username']
    auth.logout(request) # 清除用户的登录状态
    return HttpResponseRedirect(reverse('index'))