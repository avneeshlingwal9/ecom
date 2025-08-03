import json
from .models import *

def cookieCart(request):
        
        try: 
            currCart = json.loads(request.COOKIES['cart'])
        except:
            currCart = {}
        
        print("Current cart is ", currCart)
        items = []
        orders = {'order_quantity': 0 , 'order_total': 0 , 'shipping' : False}
        cartItems = orders['order_quantity']

        for i in currCart:

            try: 
            
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

                if(product.digital == False):

                    orders['shipping'] = False

            except:
                pass

        return {'cartItems': cartItems, 'order': orders , 'items':  items }
        

def cartData(request):
        
    if request.user.is_authenticated:

        customer = request.user.customer
        orders, created = Order.objects.get_or_create(customer = customer , complete = False)

        items = orders.orderitem_set.all()
        cartItems = orders.order_quantity
    else:

        cookieData =  cookieCart(request)

        cartItems = cookieData['cartItems']

        orders = cookieData['order']

        items = cookieData['items']
    
    return {'items': items , 'orders': orders , 'cart' : cartItems}


def guestOrder(request , data):
     
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)

    items = cookieData['items']


    customer, created = Customer.objects.get_or_create(email = email,)

    customer.name = name
    customer.save()


    order , created = Order.objects.get_or_create(Customer = customer , 
                            complete = False,

                            
                            )
         
    for item in items: 
             
        product = Product.objects.get(id = item['id'])
        orderItem = OrderItem.create(
        product = product,
        order = order,
        quantity = item['quantity'])

    return customer , order

    