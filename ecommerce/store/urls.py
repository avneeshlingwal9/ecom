from django.urls import path
from . import views

urlpatterns = [
    path('' , views.store , name = "store"),
    path('cart/', views.cart , name = "cart"),
    path('checkout/', views.checkout, name = "checkout"),
    path('update_items/' , views.update_items , name = "update_items"),
    path('process_order/', views.processOrder, name = "process_order"),
    path('login/', views.login_view , name="login"),
    path('register/', views.register , name = "register"),
    path('logout/', views.logout_view, name="logout_view")
]