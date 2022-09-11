from django.urls import path, include
from .views import MainView, CartView, CheckoutView, ProdDetailsView, ShopView

urlpatterns = [
                  path('', MainView, name='index'),
                  path('Cart/', CartView, name='cart'),
                  path('Product-Details/<slug>', ProdDetailsView, name='product-details'),
                  path('Checkout/', CheckoutView, name='checkout'),
                  path('Shop/<cat>/<subcat>/', ShopView),
                  path('Shop/<cat>/', ShopView),
                  path('Shop/', ShopView, name='shop'),
                  path('__debug__/', include('debug_toolbar.urls')),
              ]