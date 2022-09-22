from django.urls import path, include
from .views import MainView, CartView, CheckoutView, ProdDetailsView, ShopView, SubsribeView, ContactView, LoginView, \
    SignUpView

urlpatterns = [
                  path('', MainView, name='index'),
                  path('Cart/', CartView, name='cart'),
                  path('Product-Details/<slug>', ProdDetailsView, name='product-details'),
                  path('Product-Details/', ProdDetailsView, name='product-details'),
                  path('Checkout/', CheckoutView, name='checkout'),
                  path('Shop/<cat>/<subcat>/', ShopView),
                  path('Shop/<cat>/', ShopView),
                  path('Shop/', ShopView, name='shop'),
                  path('Subscribe/', SubsribeView, name='subscribe'),
                  path('Contact/', ContactView, name='contact'),
                  path('Login/', LoginView, name='login'),
                  path('Sign-Up/', SignUpView, name='signup'),
                  path('__debug__/', include('debug_toolbar.urls')),
              ]