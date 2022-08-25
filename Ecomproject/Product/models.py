from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe
from django.urls import reverse

class Category(models.Model):
    title = models.CharField(max_length=200)
    description= models.CharField(max_length=200)
    

    def __str__(self):
        return self.title




class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image = models.ImageField(blank=True, upload_to='product/')
    new_price = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    amount = models.IntegerField(default=0)
    detail = models.TextField()
   

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.image.url))
    image_tag.short_description = 'Image'

    def ImageUrl(self):
        if self.image:
            return self.image.url
        else:
            return ""

   

