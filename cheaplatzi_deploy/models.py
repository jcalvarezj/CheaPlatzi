from django.db import models


class ProductType(models.Model):
    name = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200,blank=False, default='')
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Ecommerce(models.Model):
    name = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200,blank=False, default='')
    url = models.CharField(max_length=200,blank=False, default='')
    image = models.CharField(max_length=200,blank=False, default='')
    country = models.CharField(max_length=70, blank=False, default='')
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    id_type_product = models.ForeignKey(ProductType,on_delete=models.CASCADE)
    id_ecommerce= models.ForeignKey(Ecommerce,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,blank=False, default='')
    description = models.TextField(blank=False, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.TextField(blank=False, default='')
    url = models.TextField(blank=False, default='')
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)