from django.urls import path
from .views import *
from .models import Category

shopUrls = list(path("Shop/" + i.type + ("/" + i.subtype if i.subtype != "None" else ""), ShopView,
                     name="Shop/" + i.type + "/" + i.subtype) for i in Category.objects.all().iterator())

urlpatterns = [
                  path('', MainView, name='index'),
                  path('Cart', CartView, name='cart'),
                  path('Product-Details', ProdDetailsView, name='product-details'),
                  path('Checkout', CheckoutView, name='checkout'),
                  path('Shop', ShopView, name='shop'),
              ] + shopUrls
