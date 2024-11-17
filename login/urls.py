from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from login import views 


app_name = 'login'
urlpatterns = [
    path('', views.login_page,name='loginPage'),
    path('register/',views.register_user, name='registerUser'),
    path('orders/', views.orders, name = 'orders'),
    path('product/', views.product, name = product)
]
urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
