
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views import View

from Product.forms import CategoryForm,ProductForm

from UserApp.forms import SignUpForm
from UserApp.models import UserProfile
from EcomApp.models import ContactMessage
from OrderApp.models import Order,OrderProduct
from Product.models import Product
from django.contrib.auth.decorators import login_required
from .forms import *

from django.contrib import messages

from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
# Create your views here.




class HomeView(View):
    def get(self,request):
        return render(request, 'base.html',{})


class CategoryView(View):
    def get(self,request):
        form=CategoryForm() #créer un formulaire vide
        return render(request,"category_form.html",{'form':form})
    def post(self,request):
        form=CategoryForm(request.POST,request.FILES) # récupérer les données saisies dans le formulaire
        if form.is_valid(): # valider les données saisies
            form.save() # sauvegarder les données dans la base de données
        return  redirect("categoryList")

class CategoryListView(View):
    def get(self,request):
        categories=Category.objects.all() #charger la liste des catégories à partir de la base de données
        return render(request,"category_list.html",{'categories':categories})


class CategoryUpdateView(View):
    def get(self,request,idp):
        category=Category.objects.get(id=idp)
        form=CategoryForm(instance=category) #créer un formulaire vide
        return render(request,"category_form.html",{'form':form})
    def post(self,request,idp):
        category=Category.objects.get(id=idp)
        form=CategoryForm(request.POST,request.FILES,instance=category) # récupérer les données saisies dans le formulaire
        if form.is_valid(): # valider les données saisies
            form.save()   # sauvegarder les données dans la base de données
        return  redirect("categoryList")


class CategoryDeleteView(View):
    def get(self,request,idp):
        return render(request,"delete_confirm.html",{})
    def post(self,request,idp):
        category=Category.objects.get(id=idp)
        category.delete()
        return  redirect("categoryList")



class ProductView(View):
    def get(self,request):
        form=ProductForm() #créer un formulaire vide
        return render(request,"product_form.html",{'form':form})
    def post(self,request):
        form=ProductForm(request.POST,request.FILES) # récupérer les données saisies dans le formulaire
        if form.is_valid(): # valider les données saisies
            form.save()   # sauvegarder les données dans la base de données
        return  redirect("productList")


class ProductListView(View):
    
    def get(self,request):
        products=Product.objects.all() #charger la liste des produits à partir de la base de données
        return render(request,"product_list.html",{'products':products})



class ProductUpdateView(View):
    def get(self,request,idp):
        prouct=Product.objects.get(id=idp)
        form=ProductForm(instance=prouct) #créer un formulaire vide
        return render(request,"product_form.html",{'form':form})
    def post(self,request,idp):
        prouct=Product.objects.get(id=idp)
        form=ProductForm(request.POST,request.FILES,instance=prouct) # récupérer les données saisies dans le formulaire
        if form.is_valid(): # valider les données saisies
            form.save()   # sauvegarder les données dans la base de données
        return  redirect("productList")


class ProductDeleteView(View):
    def get(self,request,idp):
        return render(request,"delete_confirm.html",{})
    def post(self,request,idp):
        prouct=Product.objects.get(id=idp)
        prouct.delete()
        return  redirect("productList")






def admin_login(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
           
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.userprofile.is_admin==True :
                login(request, user)
            # Redirect to a success page.
                return redirect('base')
            else:
            # Return an 'invalid login' error message.
             messages.warning(request, 'Your username or password is invalid')
        
       
        return render(request,'admin_login.html',{})



def admin_register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "user_img/1.png"
            data.is_admin=True
            
            data.save()
            return redirect('base')

        else:
            messages.warning(request,'Your passwords are not matching')
    else:
        form=SignUpForm()
    
    context = {
                'form': form }
    return render(request, 'admin_register.html', context)

   


def admin_logout(request):
    logout(request)
    return redirect('base')




def UserListView(request):
        profils=UserProfile.objects.all() 
        return render(request,"user_list.html",{'profils':profils})



class UserDeleteView(View):
    def get(self,request,idp):
        return render(request,"delete_confirm.html",{})
    def post(self,request,idp):
        profil=UserProfile.objects.get(id=idp)
        profil.delete()
        return  redirect("userList")



def AdminListView(request):
        admins=UserProfile.objects.all() 
        return render(request,"admin_list.html",{'admins':admins})




class OrderListView(View):
    def get(self,request):
        orders=Order.objects.all() #charger la liste des produits à partir de la base de données
        return render(request,"order_list.html",{'orders':orders})



class OrderDeleteView(View):
    def get(self,request,idp):
        return render(request,"delete_confirm.html",{})
    def post(self,request,idp):
        order=Order.objects.get(id=idp)
        order.delete()
        return  redirect("orderList")



class OrderUpdateView(View):
    def get(self,request,idp):
        order=Order.objects.get(id=idp)
        form=OrderUpdateForm(instance=order) #créer un formulaire vide
        return render(request,"order_formu.html",{'form':form})
    def post(self,request,idp):
        order=Order.objects.get(id=idp)
        form=OrderUpdateForm(request.POST,request.FILES,instance=order) # récupérer les données saisies dans le formulaire
        if form.is_valid(): # valider les données saisies
            form.save()   # sauvegarder les données dans la base de données
        return  redirect("orderList")


class OrderDetailsView(View):
    def get(self,request,idp):
        order=Order.objects.get(id=idp)
        orderitems=OrderProduct.objects.filter(order=order.id)
        
        return render(request,"order_details.html",{'orderitems':orderitems})



class MessageListView(View):
    def get(self,request):
        messages=ContactMessage.objects.all() #charger la liste des produits à partir de la base de données
        return render(request,"message_list.html",{'messages':messages})



class MessageDeleteView(View):
    def get(self,request,idp):
        return render(request,"delete_confirm.html",{})
    def post(self,request,idp):
        message=ContactMessage.objects.get(id=idp)
        message.delete()
        return  redirect("messageList")



class MessageUpdateView(View):
    def get(self,request,idp):
        message=ContactMessage.objects.get(id=idp)
        form=ContactUpdateForm(instance=message) #créer un formulaire vide
        return render(request,"message_form.html",{'form':form})
    def post(self,request,idp):
        message=ContactMessage.objects.get(id=idp)
        form=ContactUpdateForm(request.POST,request.FILES,instance=message) # récupérer les données saisies dans le formulaire
        if form.is_valid(): # valider les données saisies
            form.save()   # sauvegarder les données dans la base de données
        return  redirect("messageList")