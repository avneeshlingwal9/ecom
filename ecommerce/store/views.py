from django.shortcuts import render

from .models import *
# Create your views here.
def store(request):
    products = Product.objects.all()
    context = {'products' : products}

    return render(request , 'store/store.html' , context)

def cart(request):
    
    if request.user.is_authenticated:

        customer = request.user.customer
        orders, created = Order.objects.get_or_create(customer = customer , complete = False)

        items = orders.orderitem_set.all()

    else:

        items = []
        orders = {'order_quantity': 0 , 'order_total': 0}

    context  = {'items': items , 'orders' : orders}






    return render(request, 'store/cart.html', context)

def checkout(request):

    if request.user.is_authenticated:

        customer = request.user.customer
        orders, created = Order.objects.get_or_create(customer = customer , complete = False)

        items = orders.orderitem_set.all()
    else:

        items = []
        orders = {'order_quantity' : 0 , 'order_total': 0}
    
    context = {'items': items , 'orders': orders}

    return render(request, 'store/checkout.html' , context)