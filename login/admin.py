from django.contrib import admin
from . models import Product , Order , OrdersUsers , ProductOrders

# Register your models here.
admin.site.register(Product)
admin.site.register(Order) 
admin.site.register(OrdersUsers) 
admin.site.register(ProductOrders)