import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
users = [
    {"name": "test1", "pwd": "test1"},
    {"name": "test2", "pwd": "test2"}
]

def index(request):
    return render(request, 'login.html')

def login_action(request):
    if request.method =="POST":
        body = request.body
        request_data = json.loads(body)
        if "name" not in request_data or "pwd" not in request_data:
            return JsonResponse({"success": False}, safe=False)
        name = request_data["name"]
        pwd = request_data["pwd"]

        for user in users:
            if user["name"] == name and user["pwd"] == pwd:
                return JsonResponse({"success": True}, safe=False)
            else:
                return JsonResponse({"success": False}, safe=False)
    else:
        return HttpResponse("404")