from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserApp
from django.contrib.auth import authenticate, login, logout



# Create your views here.
def index(request):
    return HttpResponse("Hello")
def login_page(request):
    if(request.method == "POST"):
        name = request.POST.get('username')
        passwrd = request.POST.get('password')
        print(name, passwrd)
        user = authenticate(username=name,password = passwrd)
        if user is not None :
            login(request, user)
            return redirect('firstpage.html')
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')
def first_page(request):
    return render(request,'firstpage.html')