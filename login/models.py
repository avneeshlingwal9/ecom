from django.db import models

# Create your models here.
class UserApp(models.Model):
    name = models.CharField(max_length=200)
    passwrd = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    
