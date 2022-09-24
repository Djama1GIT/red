from django.urls import path, include
from django.contrib.auth import views
from .views import MainView, CartView, CheckoutView, ProdDetailsView, ShopView, SubsribeView, ContactView, \
    myLoginView, SignUpView, myLogoutView

urlpatterns = [
                  path('', MainView, name='index'),
                  path('Login/', myLoginView.as_view(), name='login'),
                  path('Logout/', myLogoutView.as_view(), name='logout'),
                  path('Sign-Up/', SignUpView.as_view(), name='signup'),
                  path('Cart/', CartView, name='cart'),
                  path('Product-Details/<slug>', ProdDetailsView, name='product-details'),
                  path('Product-Details/', ProdDetailsView, name='product-details'),
                  path('Checkout/', CheckoutView, name='checkout'),
                  path('Shop/<cat>/<subcat>/', ShopView),
                  path('Shop/<cat>/', ShopView),
                  path('Shop/', ShopView, name='shop'),
                  path('Subscribe/', SubsribeView, name='subscribe'),
                  path('Contact/', ContactView, name='contact'),
                  path('__debug__/', include('debug_toolbar.urls')),
              ]