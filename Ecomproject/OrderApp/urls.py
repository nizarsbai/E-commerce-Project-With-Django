
from django.urls import path
from . import views

urlpatterns = [
     path('addingcart/<int:id>/', views.Add_to_Shoping_cart, name='Add_to_Shoping_cart'),
     path('cart_details/', views.cart_detailsView, name='cart_details'),
     path('cart_delete/<int:id>/', views.cart_delete, name='cart_delete'),
     path('cart_update/<int:idp>/', views.CartUpdateView.as_view(),name='cart_update'),
     path('order_cart/', views.OrderCart, name='OrderCart'),

]