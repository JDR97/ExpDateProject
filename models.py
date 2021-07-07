from __future__ import unicode_literals
from django.db import models
#from django.contrib.auth.models import *
#from .models import *


# Create your models here.
class Customers(models.Model):
    customer = models.CharField(max_length=30)
    email = models.EmailField(max_length=25)
    contact = models.BigIntegerField()


class Users(models.Model):
    userid = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=25)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    gender = models.CharField(max_length=8)
    contact = models.BigIntegerField()
    country = models.CharField(max_length=25)
    state = models.CharField(max_length=30)
    pincode = models.CharField(max_length=12)
    image = models.ImageField(null=True, blank=True, upload_to='images/')


class ProductDB(models.Model):
    uname = models.CharField(max_length=25, default='Invalid User')
    pname = models.CharField(max_length=30)
    pdate = models.DateTimeField()
    sharing = models.BooleanField(default=0)


class Contacting(models.Model):
    sender = models.CharField(max_length=30)
    receiver = models.CharField(max_length=30)
    attime = models.DateTimeField()
    message = models.TextField(blank=True, default='No messages')

