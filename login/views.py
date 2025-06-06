from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from . import forms
from django.http import HttpResponse
from django.contrib import messages
from . import models 
from itertools import groupby
from operator import itemgetter

from django.contrib.auth.decorators import login_required




# Create your views here.
def homepage(request):
    return render(request,'login/homepage.html')
def login_page(request):
    if request.method == "POST":

        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            
            messages.success(request, "Login successful")
            login(request,form.get_user())
            if 'nxt' in request.POST:
                return redirect(request.POST.get('nxt'))

            else:
                return redirect('login:orders')
        else:
            messages.error(request, "Incorrect username or password")
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
@login_required(login_url='login:loginPage')
def orders_page(request):
    if request.method == "POST":
        check = request.POST.getlist('chk[]')
        if not check:
            return render(request, 'login/fail.html')
            raise ValueError("please select something")
            
        totalPrice = 0 
        order = models.Order.objects.create()
        selected_products = models.Product.objects.filter(product_id__in = check)
        product_map = {str(product.product_id): product for product in selected_products}
        for product_id in check:
            quantity = request.POST.get(product_id)
            if not quantity:
                return render(request, 'login/fail.html')
                raise ValueError("Empty cart")
            if not quantity.isdigit() or int(quantity) <= 0 :
                return render(request, 'login/fail.html')
                raise ValueError("Empty")
            curr_product = product_map.get(product_id)
            totalPrice+= quantity*curr_product.price
            models.ProductOrders.objects.create(
                product_id=curr_product,
                order_id= order,
                quantity= quantity
            )
        order.totalPrice = totalPrice
        order.save()
        userOrders = models.OrdersUsers.objects.create(order_id= order , username= request.user)        
        messages.success(request, "Order placed successfully")
        return redirect('login:orders')
    products = models.Product.objects.all()
    context = {'products':products }

    return render(request,'login/order.html', context)
def product_insertion(request):
    if request.method == "POST":
        product = forms.ProductCreation(request.POST,request.FILES)
        if product.is_valid():
            product.save()
        
    else:
        product = forms.ProductCreation()


    return render(request, 'login/products.html' , {'form' : product})
@login_required(login_url='login:loginPage')
def order_history(request):
    variety = models.Product.objects.values_list('product_type',flat=True).distinct()
    selected_type = request.POST.get('selected_type')

    order = models.ProductOrders.objects.select_related('product_id', 'order_id').filter(order_id__ordersusers__username = request.user).order_by('order_id')
    order_groups = []
    
    if selected_type :
        order = order.filter(product_id__product_type=selected_type)

    for order_id, group in groupby(order,key = lambda x: x.order_id):
        groups_list = list(group)
        total = sum(item.product_id.price*item.quantity  for item in groups_list)
        order_groups.append({
            'order_id' : order_id,
            'products_list' : groups_list,
            'total_price': total}
        )

    


    context = {'product_type' : variety , 'order_groups': order_groups,  'selected_type': selected_type }

    return render(request, 'login/order_history.html', context)



"""   for  product_id in check:
        quantity = request.POST.get(product_id)
        currProduct = models.Product.objects.filter(product_id= product_id)
        totalPrice += currProduct[0].price*float(quantity)
        productOrders = models.ProductOrders(order_id= order.order_id , product_id= product_id ,quantity= quantity )
        productOrders.save() """
'''  orders_list = order.values_list('order_id',flat=True)
    products_list = models.Product.objects.filter(productorders__order_id__in = orders_list)'''