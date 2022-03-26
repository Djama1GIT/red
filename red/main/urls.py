from django.urls import path
from .views import *

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('cart', CartView.as_view(), name='cart'),
    path('product-details', ProdDetailsView.as_view(), name='product-details'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('shop', ShopView.as_view(), name='shop'),
]