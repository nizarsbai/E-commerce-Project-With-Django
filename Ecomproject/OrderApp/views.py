from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from Product.models import Category
from EcomApp.models import *
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from UserApp.models import UserProfile
# Create your views here.

@login_required(login_url='/user/login')
def Add_to_Shoping_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    checking = ShopCart.objects.filter(
        product_id=id, user_id=current_user.id)
    if checking:
        control = 1
    else:
        control = 0

    if request.method == "POST":
        form = ShopingCartForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = ShopCart.objects.filter(
                    product_id=id, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, 'Your Product  has been added successfuly')
        return HttpResponseRedirect(url)
    else:
        if control == 1:
            data = ShopCart.objects.filter(
                product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, 'Your  product has been added successfuly')
        return HttpResponseRedirect(url)


@login_required(login_url='/user/login')
def cart_detailsView(request):
        current_user = request.user
        category = Category.objects.all()
        
        cart_products= ShopCart.objects.filter(user_id=current_user.id)
        total_amount = 0
        for p in cart_products:
            total_amount += p.amount()
        
        total_quan = 0
        for p in cart_products:
            total_quan += p.quantity

        context={ 'category': category,
                 
                  'cart_products' : cart_products,
                  'total' : total_amount,
                  'total_quan':total_quan,

        }
        return render(request,'cart_details.html',context)


def cart_delete(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    cart_product = ShopCart.objects.filter(id=id, user_id=current_user.id)
    cart_product.delete()
    messages.warning(request, 'Your product has been deleted from cart')
   
    return HttpResponseRedirect(url)



class CartUpdateView(View):
    def get(self,request,idp):
        cart=ShopCart.objects.get(id=idp)
        form=ShopingCartForm(instance=cart) #créer un formulaire vide
        return render(request,"cart_form.html",{'form':form})
    def post(self,request,idp):
        cart=ShopCart.objects.get(id=idp)
        form=ShopingCartForm(request.POST,request.FILES,instance=cart) # récupérer les données saisies dans le formulaire
        if form.is_valid(): # valider les données saisies
            form.save()   # sauvegarder les données dans la base de données
        return  redirect('cart_details')



   



@login_required(login_url='/user/login')
def OrderCart(request):
    current_user = request.user
    shoping_cart = ShopCart.objects.filter(user_id=current_user.id)
    totalamount = 0
    for rs in shoping_cart:
        totalamount += rs.quantity * rs.product.new_price
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            dat = Order()
            # get product quantity from form
            dat.first_name = form.cleaned_data['first_name']
            dat.last_name = form.cleaned_data['last_name']
            dat.address = form.cleaned_data['address']
            dat.city = form.cleaned_data['city']
            dat.phone = form.cleaned_data['phone']
            dat.country = form.cleaned_data['country']
            dat.user_id = current_user.id
            dat.total = totalamount
            ordercode = get_random_string(5).upper()  # random cod
            dat.code = ordercode
            dat.save()

            # moving data shortcart to product cart
            for rs in shoping_cart:
                data = OrderProduct()
                data.order_id = dat.id
                data.product_id = rs.product_id
                data.user_id = current_user.id
                data.quantity = rs.quantity
                data.price = rs.product.new_price
                data.amount = rs.amount
                data.save()

                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()
            # Now remove all Order data from the shoping cart
            ShopCart.objects.filter(user_id=current_user.id).delete()
            # request.session['cart_item']=0
            messages.success(request, 'Your Order has been completed')
            category = Category.objects.all()
           
            context = {
                'total': totalamount,
                'ordercode': ordercode,
                'category': category,
                }

            return render(request, 'order_completed.html', context)
        else:
            messages.warning(request, form.errors)
          #  return HttpResponseRedirect("/order/Order_cart")
    form = OrderForm()
   
    cart_products = ShopCart.objects.filter(user_id=current_user.id)
    
    total_quan = 0
    for p in shoping_cart:
            total_quan += p.quantity
    category = Category.objects.all()
    

    context = {
        
        'shoping_cart': shoping_cart,
        'total': totalamount,
        
        'form': form,
        'category': category,
       
        'total_quan':total_quan,
        'cart_products':cart_products,
    }
    return render(request, 'order_form.html', context)




