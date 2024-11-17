from django.db import models
from djmoney.models.fields import MoneyField

# Create your models here.

class Product(models.Model):
    product_id = models.CharField(blank=False, null=False, max_length=10)
    image = models.ImageField(default = 'product.png' , upload_to = 'product_img/')
    product_type = models.CharField( max_length=40)
    product_name = models.TextField(default="pname")
    price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='INR',
        max_digits=11)
    def __str__(self):
        return self.product_name
    






    
