from django.db import models
from djmoney.models.fields import Money

# Create your models here.

class Product(models.Model):
    product_id = models.CharField(required = True, max_length=10)
    image = models.ImageField(default = 'product.png')
    product_type = models.CharField(required = True , max_length=40)
    price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='INR',
        max_digits=11)





    
