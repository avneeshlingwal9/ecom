from django.shortcuts import render
from django.http import HttpResponse
from .models import UserApp

# Create your views here.
def index(request):
    return HttpResponse("Hello")
def login_page(request):
    if(request.method == "POST"):
        name = request.POST.get('username')
        passwrd = request.POST.get('password')
        user = UserApp(name=name, passwrd=passwrd)
        user.save()
    return render(request, 'login.html')
