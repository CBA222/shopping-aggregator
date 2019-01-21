from django.db import models
from django.contrib.postgres import fields

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    image_url = models.URLField(default='no-image')
    description = models.CharField(max_length=10000, default="")
    upc = models.CharField(max_length=100, default="")
    model_number = models.CharField(max_length=100, default="")
    listings = fields.JSONField(default=[])

    best_vendor = models.CharField(max_length=50, default="")
    best_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    best_url = models.URLField(max_length=500, default='no-url')


    #price = models.DecimalField(max_digits=10, decimal_places=2)
    #url = models.URLField(default='no-url')
    
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=200)


class Vendor(models.Model):
    name = models.CharField(max_length=200)