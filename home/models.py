from django.db import models

# Create your models here.

class contact(models.Model):
    name= models.CharField( max_length= 50 ,blank=False)
    email= models.EmailField( max_length=254, blank=False)
    message = models.TextField(max_length = 100, default='No Description')

