from django import forms
from django.forms.widgets import Textarea
from .models import *
from django.forms import  TextInput, EmailInput

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email' ,'subject', 'message']
        widgets = {
           
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'Name & Surname'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'Write your email'}),
            'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Write your Subject'}),
            'message': Textarea(attrs={'class': 'input', 'placeholder': 'Write your message'}),
        }

        
class SearchForm(forms.Form):
    query= forms.CharField(max_length=200)
    cat_id= forms.IntegerField()