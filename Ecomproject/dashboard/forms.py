from EcomApp.models import ContactMessage
from Product.models import Category
from OrderApp.models import Order
from django import forms


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status',]
        

class ContactUpdateForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['status','Note',]
        