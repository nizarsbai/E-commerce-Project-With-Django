from django import views
from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse, request
from django.contrib import messages
from .forms import *
from EcomApp.models import *
from OrderApp.models import ShopCart
from Product.models import Product, Category
from Product.forms import CategoryForm
from UserApp.models import UserProfile
from django.contrib.auth.decorators import user_passes_test

# Create your views here.







class HomeView(View):
    def get(self,request):
        current_user = request.user
        cart_products = ShopCart.objects.filter(user_id=current_user.id)
        
        
        total_amount = 0
        for p in cart_products:
            total_amount += p.amount()
        total_quan = 0
        for p in cart_products:
             total_quan += p.quantity

        category = Category.objects.all()
      
       
        latest_products = Product.objects.all().order_by('-id')
        products=Product.objects.order_by('id')

        context={
                 'latest_products' : latest_products,
                 'products' : products,
                 'category' : category,
                 'cart_products' : cart_products,
                 'total' : total_amount,
                 'total_quan': total_quan,
                
                 }
        return render(request, 'home.html',context)


class ProductView(View):

    def get(self,request,id):
        current_user = request.user
        
        cart_products = ShopCart.objects.filter(user_id=current_user.id)
        total_amount = 0
        for p in cart_products:
            total_amount += p.amount()
        total_quan = 0
        for p in cart_products:
             total_quan += p.quantity

        
        single_product=  Product.objects.get(id=id)
       
        products = Product.objects.all().order_by('id')[:6]

        context={
                 'single_product' : single_product,
                
                 'products' : products,
                 'cart_products' : cart_products,
                 'total' : total_amount,
                 'total_quan' : total_quan,}

        return render(request,'product-single.html',context)


class Category_productView(View):

    def get(self,request,id):
        current_user = request.user
        cart_products = ShopCart.objects.filter(user_id=current_user.id)
        
        total_amount = 0
        for p in cart_products:
            total_amount += p.amount()

        total_quan = 0
        for p in cart_products:
             total_quan += p.quantity
        category = Category.objects.all()
       
        product_cat = Product.objects.filter(category_id=id)
        context={
            'product_cat' : product_cat,
            
            'category' : category,
            'cart_products' : cart_products,
            'total' : total_amount,
            'total_quan': total_quan,
        }
        return render(request,'category_products.html',context)

class aboutusView(View):
    
    def get(self,request):
        current_user = request.user
        cart_products = ShopCart.objects.filter(user_id=current_user.id)
       
        total_amount = 0
        for p in cart_products:
            total_amount += p.amount()
        
        total_quan = 0
        for p in cart_products:
             total_quan += p.quantity
        
        category = Category.objects.all()
    
        context={
                 'category' : category,
                 'cart_products' : cart_products,
                 'total' : total_amount,
                 'total_quan': total_quan,
                
        }
        return render(request, 'aboutus.html', context)


class ContactView(View):
    def get(self,request):
        current_user = request.user
        cart_products = ShopCart.objects.filter(user_id=current_user.id)
       
        total_amount = 0
        for p in cart_products:
            total_amount += p.amount()
        total_quan = 0
        for p in cart_products:
             total_quan += p.quantity
        form = ContactForm()
        category = Category.objects.all()
        
        context={'form':form ,'category' : category,'cart_products' : cart_products,
                 'total' : total_amount , 'total_quan': total_quan,}

        return render(request, 'contactus.html', context)
    
    def post(self,request):
        form= ContactForm(request.POST,request.FILES)
        if form.is_valid():
            data = ContactMessage()
            data.name=form.cleaned_data['name']
            data.email=form.cleaned_data['email']
            data.subject=form.cleaned_data['subject']
            data.message=form.cleaned_data['message']
            data.save()
        messages.success(request,"Your message has been sent. Thank you for your message.")
            
        return redirect('contactus')
            
def SearchView(request):
    if request.method=='POST':

        form= SearchForm(request.POST,request.FILES)
        if form.is_valid():
            query= form.cleaned_data['query']
            cat_id= form.cleaned_data['cat_id']
            if cat_id == 0:
                products= Product.objects.filter(title__icontains=query)
           
            else:
                products= Product.objects.filter(title__icontains=query , category_id=cat_id)
                
           
            category = Category.objects.all()
            current_user = request.user
            cart_products = ShopCart.objects.filter(user_id=current_user.id)
            total_amount = 0
            for p in cart_products:
                total_amount += p.amount()
            
            total_quan = 0
            for p in cart_products:
                total_quan += p.quantity

            context= {
                'category' : category,
                'query' : query,
                'product_cat' : products,
                
                'cart_products' : cart_products,
                'total' : total_amount,
                'total_quan': total_quan,
            }

            return render(request, 'category_products.html', context)

    return HttpResponseRedirect('home')



class ProductsView(View):
     def get(self,request):
        current_user = request.user
        cart_products = ShopCart.objects.filter(user_id=current_user.id)
        
        total_amount = 0
        for p in cart_products:
            total_amount += p.amount()
        total_quan = 0
        for p in cart_products:
             total_quan += p.quantity
        
        
        products = Product.objects.all()
        category = Category.objects.all()
        context={
                 'category':category,
                 'products' : products,
                 'cart_products' : cart_products,
                 'total' : total_amount,
                  'total_quan': total_quan,
                  }

        return render(request,'products.html',context)


class FAQView(View):
    def get(self,request):
        current_user = request.user
        cart_products = ShopCart.objects.filter(user_id=current_user.id)
       
        total_amount = 0
        for p in cart_products:
            total_amount += p.amount()
        total_quan = 0
        for p in cart_products:
             total_quan += p.quantity
        
        
       
        category = Category.objects.all()
        context={
                 'category':category,
                 
                 'cart_products' : cart_products,
                 'total' : total_amount,
                  'total_quan': total_quan,}
        return render(request,'faq.html',context)

    
