from django.shortcuts import render
from .models import *

phone_number = "+79991234567"
phone_number_ed = "+7(999)123-45-67"


def MainView(request):
    promos = Promo.objects.filter(access="all")
    promos_width = str(100 / (promos.count()+1))[:9]
    return render(request, 'red/index.html', {'title': 'RED | Home Page', 'phone': phone_number,
                                              'phone_ed': phone_number_ed, 'promos': promos,
                                              'promos_width': promos_width})


def CartView(request):
    return render(request, 'red/cart.html', {'title': 'RED | Cart', 'phone': phone_number,
                                             'phone_ed': phone_number_ed})


def ProdDetailsView(request):
    return render(request, 'red/product-details.html', {'title': 'RED | Product Details', 'phone': phone_number,
                                                        'phone_ed': phone_number_ed})


def CheckoutView(request):
    return render(request, 'red/checkout.html', {'title': 'RED | Checkout Page', 'phone': phone_number,
                                                 'phone_ed': phone_number_ed})


def ShopView(request):
    return render(request, 'red/shop.html', {'title': 'RED | Shop', 'phone': phone_number,
                                             'phone_ed': phone_number_ed})
