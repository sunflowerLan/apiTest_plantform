from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')


def try_vue(request):
    return render(request, 'tryVue.html')


def com_demo(request):
    return render(request, 'vcomponent.html')