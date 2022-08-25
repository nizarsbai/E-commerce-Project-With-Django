from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(), name='home'),
    path('aboutus/',views.aboutusView.as_view(),name='aboutus'),
    path('contactus/',views.ContactView.as_view(),name='contactus'),
    path('product/<int:id>',views.ProductView.as_view(), name='product-detail'),
    path('products/<int:id>/',views.Category_productView.as_view(), name='category_product'),
    path('search/', views.SearchView,name="search"),
    path('allproducts/',views.ProductsView.as_view(),name="products"),
    path('FAQ/',views.FAQView.as_view(), name='faq'),


    
]