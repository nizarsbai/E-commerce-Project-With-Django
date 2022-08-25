from django.shortcuts import render,redirect
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from .forms import *
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import user_passes_test
# Create your views here.
from Product.models import Category
from OrderApp.models import ShopCart
from EcomApp.models import *






def user_logout(request):
    logout(request)
    return redirect('home')


def user_login(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
           
            user = authenticate(request, username=username, password=password)
            
            if user is not None  and user.userprofile.is_costumer==True :
                login(request, user)
            # Redirect to a success page.
                return redirect('home')
            else:
            # Return an 'invalid login' error message.
             messages.warning(request, 'Your username or password is invalid')
        
        category = Category.objects.all()
       
        
        context={'category' : category,
                  
                  }
        return render(request,'user_login.html',context)


def user_register(request):
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
            data.is_costumer=True
            
            data.save()
            return redirect('home')

        else:
            messages.warning(request,'Your passwords are not matching')
    else:
        form=SignUpForm()
    category = Category.objects.all()
    
    context = {'category' : category,
                
                'form': form }
    return render(request, 'user_register.html', context)

def userprofile(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    cart_products= ShopCart.objects.filter(user_id=current_user.id)
    total_amount = 0
    for p in cart_products:
        total_amount += p.amount()

    total_quan = 0
    for p in cart_products:
        total_quan += p.quantity


    context = {'category': category,
               
               'profile': profile,
               'total': total_amount,
               'total_quan':total_quan,
               'cart_products':cart_products,
               }
    return render(request, 'user_profile.html', context)



@login_required(login_url='/user/login')  # Check login
def user_update(request):
    if request.method == 'POST':
        # request.user is user  data
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('userprofile')
    else:
      
        user_form = UserUpdateForm(instance=request.user)
       
        profile_form = ProfileUpdateForm(instance=request.user)
        current_user = request.user
        category = Category.objects.all()
       

        cart_products= ShopCart.objects.filter(user_id=current_user.id)
        total_amount = 0
        for p in cart_products:
            total_amount += p.amount()

        total_quan = 0
        for p in cart_products:
            total_quan += p.quantity

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'category': category,
            
            'total': total_amount,
            'total_quan':total_quan,
            'cart_products':cart_products,
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/user/login')  # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('userprofile')
        else:
            messages.error(
                request, 'Please correct the error below.<br>' + str(form.errors))
            return redirect('user_password')
    else:
        category = Category.objects.all()
        
        form = PasswordChangeForm(request.user)
        current_user=request.user
        cart_products= ShopCart.objects.filter(user_id=current_user.id)
        total_amount = 0
        for p in cart_products:
            total_amount += p.amount()

        total_quan = 0
        for p in cart_products:
            total_quan += p.quantity
        return render(request, 'user_password_update.html', {'form': form,
                                                           'category': category,
                                                           
                                                           'total': total_amount,
                                                            'total_quan':total_quan,
                                                            'cart_products':cart_products,

                                                           })

