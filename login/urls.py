from django.contrib import admin
from django.urls import path
from login import views 

urlpatterns = [
    path('', views.index,name='home'),
    path('login/', views.login_page,name='loginuser'),
    path('firstpage/',views.first_page, name='firstpage')
]