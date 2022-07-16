from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserDetailsModel(AbstractUser):
    mobile = models.CharField(max_length=100,blank=True,null=True)
    status = models.CharField(max_length=100,blank=True,null=True,default="Active")
    usertype = models.CharField(max_length=255,blank=True,null=True)
    showpassword = models.CharField(max_length=100,blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)