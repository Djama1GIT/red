from django.urls import path, include
from .views import MainView, CartView, CheckoutView, ProdDetailsView, ShopListView, SubscribeView, ContactView, \
    MyLoginView, SignUpView, MyLogoutView, PurchasesView, SettingsView, ChangePhotoView, EmailVerificationView

urlpatterns = [
                  path('', MainView.as_view(), name='index'),
                  path('Login/', MyLoginView.as_view(), name='login'),
                  path('Logout/', MyLogoutView.as_view(), name='logout'),
                  path('Sign-Up/', SignUpView.as_view(), name='signup'),
                  path('Verify/<email>/<uuid:code>', EmailVerificationView.as_view(), name='email_verification'),
                  path('Cart/', CartView.as_view(), name='cart'),
                  path('Product-Details/<slug>', ProdDetailsView, name='product-details'),
                  path('Product-Details/', ProdDetailsView, name='product-details'),
                  path('Checkout/', CheckoutView.as_view(), name='checkout'),
                  path('Purchases/', PurchasesView.as_view(), name='purchases'),
                  path('Shop/<type>/<subtype>/', ShopListView.as_view()),
                  path('Shop/<type>/', ShopListView.as_view()),
                  path('Shop/', ShopListView.as_view(), name='shop'),
                  path('Subscribe/', SubscribeView.as_view(), name='subscribe'),
                  path('Contact/', ContactView.as_view(), name='contact'),
                  path('Settings/', SettingsView.as_view(), name='settings'),
                  path('admin/main/change-photo/<what>/<slug>', ChangePhotoView.as_view(), name='change-photo'),
                  path('__debug__/', include('debug_toolbar.urls')),
              ]