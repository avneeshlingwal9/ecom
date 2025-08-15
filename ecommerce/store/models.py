from django.db import models

from django.contrib.auth.models import User
# Create your models here.

# Customer model with name, and email and is refering to the django model. 

class Customer(models.Model):

    user = models.OneToOneField(User, null = True , blank = True, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200 , null = True)
    email = models.CharField(max_length = 200)

    def __str__(self):
        return self.name

# Product containing name, price, digital and image. 
# Contains two properties: 
# imgURL, for the url of the image.     

class Product(models.Model):

    name = models.CharField(max_length=200 )
    price = models.FloatField()
    digital = models.BooleanField(default=False , null= True , blank = True)
    image = models.ImageField(null= True, blank = True)

    def __str__(self):
        return self.name
    
    @property
    def imgURL(self):
        
        try: 
            url = self.image.url
        except:
            url = ''
        return url

# Order refering to customer, containing fields such as date_ordered_, complete flag and transaction_id. 
# Property: order_total => Getting the total amount of the order. 
# Property: order_quantity => Getting the total quantity of the order. 
# Property: isShipping => If the order contains a product which needs shipping. 

class Order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null= True , blank = True)
    date_ordered = models.DateTimeField(auto_now_add = True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    
    @property

    def order_total(self):
        items = self.orderitem_set.all()
        total = sum([item.item_total for item in items])

        return total

    @property

    def order_quantity(self):

        items = self.orderitem_set.all()
        total = sum([item.quantity for item in items])
        return total
    
    @property

    def isShipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()
        for i in orderItems: 
            if i.product.digital == False:
                shipping = True
        
        return shipping

# OrderItem for a particular item in the order. 
# References to product, order, quantity, and also date added. 
# Property: item_total() => Returns the total amount of the orderitem. 

class OrderItem(models.Model):

    product = models.ForeignKey(Product, on_delete= models.SET_NULL , null = True)
    order = models.ForeignKey(Order , on_delete=models.SET_NULL , null=True)
    quantity = models.IntegerField(default=0 , null = True,  blank = True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def item_total(self):

        return self.product.price * self.quantity

# Shipping Address. 
# Contains customer, order, address, city, state, zipcode and date_added. 

class ShippingAddress(models.Model):

    customer = models.ForeignKey(Customer , on_delete=models.SET_NULL , null = True)
    order = models.ForeignKey(Order , on_delete=models.SET_NULL , null = True)
    address = models.CharField(max_length=200 , null= False)
    city = models.CharField(max_length=200,null= False)
    state = models.CharField(max_length=200 , null=False)
    zipcode = models.CharField(max_length=200 , null= False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
