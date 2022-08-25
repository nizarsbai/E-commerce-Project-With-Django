from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(), name='base'),
    path('categories/create', views.CategoryView.as_view(),name="categoryCreate"),
    path('categories/', views.CategoryListView.as_view(),name="categoryList"),
    path('categories/<int:idp>/update', views.CategoryUpdateView.as_view(),name="categoryUpdate"),
    path('categories/<int:idp>/delete', views.CategoryDeleteView.as_view(),name="categoryDelete"),
    path('products/create', views.ProductView.as_view(),name="productCreate"),
    path('products/', views.ProductListView.as_view(),name="productList"),
    path('products/<int:idp>/update', views.ProductUpdateView.as_view(),name="productUpdate"),
    path('products/<int:idp>/delete', views.ProductDeleteView.as_view(),name="productDelete"),
    path('login/', views.admin_login, name='admin_login'),
    path('register/', views.admin_register, name='admin_register'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('users/', views.UserListView,name="userList"),
    path('users/<int:idp>/delete', views.UserDeleteView.as_view(),name="userDelete"),
    path('admins/', views.AdminListView,name="adminList"),
    path('orders/', views.OrderListView.as_view(),name="orderList"),
    path('orders/<int:idp>/delete', views.OrderDeleteView.as_view(),name="orderDelete"),
    path('orders/<int:idp>/update', views.OrderUpdateView.as_view(),name="orderUpdate"),
    path('orders/<int:idp>/details', views.OrderDetailsView.as_view(),name="orderDetails"),
    path('messages/', views.MessageListView.as_view(),name="messageList"),
    path('messages/<int:idp>/delete', views.MessageDeleteView.as_view(),name="messageDelete"),
    path('messages/<int:idp>/update', views.MessageUpdateView.as_view(),name="messageUpdate"),
    
]