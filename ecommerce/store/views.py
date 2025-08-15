from django.shortcuts import render, redirect

from django.http import JsonResponse
from .models import *
import json
import datetime
from .utils import *
from .forms import *

from django.contrib.auth import login, authenticate, logout
# Create your views here.


def store(request):
    
    data = cartData(request)

    cartItems = data['cart']
    orders = data['orders']
    items = data['items']

    products = Product.objects.all()
    

    context = {'products': products , 'cart' : cartItems}
    
    return render(request , 'store/store.html' , context)

def cart(request):

    data = cartData(request)

    cartItems = data['cart']
    orders = data['orders']
    items = data['items']


    



    context  = {'items': items , 'orders' : orders , 'cart': cartItems }






    return render(request, 'store/cart.html', context)

def checkout(request):

    data = cartData(request)

    cartItems = data['cart']
    orders = data['orders']
    items = data['items']

    context = {'items': items , 'orders': orders , 'cart': cartItems}

    return render(request, 'store/checkout.html' , context)

def update_items(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action ', action)
    print('Product id ', productId)
    customer = request.user.customer
    product = Product.objects.get(id = productId)

    order, created = Order.objects.get_or_create(customer = customer , complete = False)

    orderitem , created = OrderItem.objects.get_or_create(order = order , product = product)

    if action == "add":
        orderitem.quantity = orderitem.quantity + 1 
    elif action == "remove":
        orderitem.quantity = orderitem.quantity - 1 

    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()
    

    return JsonResponse('Item was added' , safe=False)


def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()

    data = json.loads(request.body)

    if request.user.is_authenticated:
         customer = request.user.customer
         order, created = Order.objects.get_or_create(customer = customer, complete = False)
         
    else:
         print("User is not logged in")
         print("Cookies: ", request.COOKIES)

         customer, order = guestOrder(request, data) 
        

    total = float(data['form']['total'])
    order.transaction_id = transaction_id



    if total == order.order_total:
        order.complete = True
    
    order.save()

    if order.isShipping:
        ShippingAddress.objects.create(
            customer = customer,
            order = order, 
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )


    
    return JsonResponse('Payment Submitted ...', safe=False)

def login_view(request):

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username = username , password = password)

            if user is not None:

                login(request, user)
            
                return redirect('store')
            
    
    
    else:
        form = LoginForm()
    context = {'form': form}

    return render(request, 'store/login.html' , context)


def register(request):

    if request.method == "POST":

        form = UserInfoForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            
            user.set_password(form.cleaned_data['password1'])

            username = form['username']
            email = form['email']

            user.save()

            customer = Customer.objects.create(user = user , name = username , email = email)
            customer.save()
            
            login(request, user)

            return redirect('store')
        
    else:

        form = UserInfoForm()




    return render(request, 'store/register.html' , {'form': form})


def logout_view(request):

    if request.user.is_authenticated: 

        logout(request)

    return redirect('store')

