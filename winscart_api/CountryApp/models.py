from django.db import models

# Create your models here.

class DialCodeModels(models.Model):
    name  = models.CharField(max_length=100,null=True,blank=True)
    dial_code  = models.CharField(max_length=100,null=True,blank=True)
    code  = models.CharField(max_length=100,null=True,blank=True)
