from django.contrib import admin

from .models import Product, ProductCategory, Vendor

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Vendor)