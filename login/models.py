from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Product(models.Model):
    product_id = models.CharField(primary_key=True, max_length=10)
    image = models.ImageField(default = 'product.jpg' , upload_to = 'product_img/')
    product_type = models.CharField( max_length=40)
    product_name = models.TextField(default="pname")
    price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='INR',
        max_digits=11)
    def __str__(self):
        return self.product_name

class Order(models.Model):

    order_id = models.AutoField( primary_key=True)
    totalPrice = MoneyField(
        decimal_places=2,
        default = 0,
        default_currency = 'INR',
        max_digits = 11
        )
    def __str__(self):
        return str(self.order_id)
    

class ProductOrders(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order_id', 'product_id'], name='unique_product_order')
        ]
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE, db_column='order_id')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null= True, db_column='product_id')
    product_ordered = models.DateField( auto_now_add=True)
    product_delivered = models.DateField(default=date(2024,1,1))
    quantity = models.PositiveIntegerField(default = 1)

    def __str__(self):
        return str(self.product_id)
    
class OrdersUsers(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order_id', 'username'], name='unique_user_order')
        ]
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE,  db_column='order_id')
    username = models.ForeignKey(User,on_delete=models.CASCADE,  db_column='username') 
    def __str__(self):
        return str(self.username)
    




    
