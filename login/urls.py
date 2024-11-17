from django.contrib import admin
from django.urls import path

from login import views 


app_name = 'login'
urlpatterns = [
    path('', views.login_page,name='loginPage'),
    path('register/',views.register_user, name='registerUser'),
    path('orders/', views.orders, name = 'orders'),
    path('product/', views.product_insertion, name= 'product')
]

