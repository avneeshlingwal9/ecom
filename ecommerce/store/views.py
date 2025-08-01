from django.shortcuts import render

from django.http import JsonResponse
from .models import *
import json
import datetime
# Create your views here.
def store(request):
    products = Product.objects.all()

    if request.user.is_authenticated:

        customer = request.user.customer
        orders , created = Order.objects.get_or_create(customer = customer , complete = False)
        cartItems = orders.order_quantity
        items = orders.order_quantity
    else:
        items = []

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

        try: 
            currCart = json.loads(request.COOKIES['cart'])
        except:
            currCart = {}
        
        print("Current cart is ", currCart)
        items = []
        orders = {'order_quantity': 0 , 'order_total': 0 , 'shipping' : False}
        cartItems = orders['order_quantity']

        for i in currCart:

            
            cartItems += currCart[i]['quantity']

            product = Product.objects.get(id = i)
            total = (product.price * float(currCart[i]['quantity']))
            


            orders['order_quantity'] += cartItems
            orders['order_total'] += total

            item = {
                'product':{
                    'id' : product.id,
                    'name': product.name,
                    'price':product.price,
                    'imageURL': product.image
                },
                'quantity': currCart[i]['quantity'],
                'item_total': total,
            }

            items.append(item)

        


	


    context  = {'items': items , 'orders' : orders , 'cart': cartItems }






    return render(request, 'store/cart.html', context)

def checkout(request):

    if request.user.is_authenticated:

        customer = request.user.customer
        orders, created = Order.objects.get_or_create(customer = customer , complete = False)

        items = orders.orderitem_set.all()
        cartItems = orders.order_quantity
    else:

        items = []
        orders = {'order_quantity' : 0 , 'order_total': 0 , 'shipping' : False}
        cartItems = orders['order_quantity']
    
    context = {'items': items , 'orders': orders , 'cart' : cartItems}

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
         total = float(data['form']['total'])
         order.transaction_id = transaction_id

    else:
         print("User is not logged in")

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