from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from login import views 


app_name = 'login'
urlpatterns = [
    path('', views.homepage, name='homePage'),
    path('login/', views.login_page,name='loginPage'),
    path('register/',views.register_user, name='registerUser'),
    path('orders/', views.orders, name = 'orders'), 
    path('product/', views.product_insertion, name= 'product'),
    path('logOut/' ,LogoutView.as_view(next_page='login:loginPage'), name= 'logOut' )
]

