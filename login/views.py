from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse





# Create your views here.
def index(request):
    return HttpResponse("Hello")
def login_page(request):
    return HttpResponse("Login page")


def firstpage(request):
    return render(request,'firstpage.html')