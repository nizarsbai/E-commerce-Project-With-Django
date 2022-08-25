from django import forms
from .models import *
from django.forms import  TextInput

class ShopingCartForm(forms.ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name',
                  'phone', 'address', 'city', 'country']