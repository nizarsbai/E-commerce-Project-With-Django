from django.contrib import admin
from Product.models import Category, Product


# Register your models here.

admin.site.register(Category)







class ProductAdmin(admin.ModelAdmin):
    list_display = ['title',  'image_tag']
    list_filter = ['title']
    list_per_page = 10
    search_fields = ['title', 'new_price', 'detail']
    




admin.site.register(Product, ProductAdmin)
