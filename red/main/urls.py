from django.urls import path
from .views import *

urlpatterns = [
    path('', MainView, name='index'),
    path('cart', CartView, name='cart'),
    path('product-details', ProdDetailsView, name='product-details'),
    path('checkout', CheckoutView, name='checkout'),
    path('shop', ShopView, name='shop'),
]