from django.shortcuts import render

from django.http import JsonResponse
from .models import *
import json
# Create your views here.
def store(request):
    products = Product.objects.all()

    if request.user.is_authenticated:

        customer = request.user.customer
        orders , created = Order.objects.get_or_create(customer = customer , complete = False)
        cartItems = orders.order_quantity
    else:

        orders = {'order_quantity' : 0}
        cartItems = orders['order_quantity']

    context = {'products': products , 'cart' : cartItems}
    
    return render(request , 'store/store.html' , context)

def cart(request):
    
    if request.user.is_authenticated:

        customer = request.user.customer
        orders, created = Order.objects.get_or_create(customer = customer , complete = False)

        items = orders.orderitem_set.all()
        cartItems = orders.order_quantity

    else:

        items = []
        orders = {'order_quantity': 0 , 'order_total': 0}
        cartItems = orders['order_quantity']

    context  = {'items': items , 'orders' : orders , 'cart': cartItems}






    return render(request, 'store/cart.html', context)

def checkout(request):

    if request.user.is_authenticated:

        customer = request.user.customer
        orders, created = Order.objects.get_or_create(customer = customer , complete = False)

        items = orders.orderitem_set.all()
        cartItems = orders.order_quantity
    else:

        items = []
        orders = {'order_quantity' : 0 , 'order_total': 0}
        cartItems = orders['order_quantity']
    
    context = {'items': items , 'orders': orders , 'cart' : cartItems}

    return render(request, 'store/checkout.html' , context)

def update_items(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id = productId)

    order, created = Order.objects.get_or_create(customer = customer , complete = False)

    orderitem , created = OrderItem.objects.get_or_create(order = order , product = product)

    if action == "add":
        orderitem.quantity = orderitem.quantity + 1 
    elif action == "remove":
        orderitem.quantity = orderitem.quantity - 1 

    if orderitem.quantity > 0:
        orderitem.save()

    return JsonResponse('Item was added' , safe=False)