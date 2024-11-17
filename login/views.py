from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from . import forms
from django.http import HttpResponse
from django.contrib import messages
from . models import Product




# Create your views here.
def login_page(request):
    if request.method == "POST":

        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            messages.success(request, "Login successful")
            login(request,form.get_user())
            return redirect('login:loggedIn')
        else:
            return render(request, 'login/home_login.html', {'form': form})
            
    else:
        form = AuthenticationForm()
    return render(request, 'login/home_login.html', {'form': form})
def register_user(request):
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            messages.success(request,"User created successfully")
            form.save()
            return redirect('login:loginPage')
        else:
            return render(request,'login/new_registeration.html', {'form' : form})
    else:
        form = forms.RegisterForm()
    return render(request, 'login/new_registeration.html', {'form': form})
def orders(request):
    return render(request, 'login/user_profilepage.html')
def product_insertion(request):
    if request.method == "POST":
        product = forms.ProductCreation(request.POST,request.FILES)
        if product.is_valid():
            product.save()
        
    else:
        product = forms.ProductCreation()


    return render(request, 'login/products.html' , {'form' : product})
