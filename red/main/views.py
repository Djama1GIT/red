from django.shortcuts import render
from django.conf import settings
from .models import *
from itertools import chain

phone_number = "+79991234567"
phone_number_ed = "+7(999)123-45-67"
twitter = "#"
facebook = "#"
linkedIn = "#"
pinterest = "#"

categories = {}
for i in Category.objects.raw('SELECT * FROM main_category').iterator():
    if i.type in categories:
        if i.subtype != "None":
            categories[i.type] += [i.subtype]
    else:
        categories[i.type] = []


def MainView(request):
    promos = Promo.objects.filter(access="all")
    fashions = Fashion.objects.all()
    fashion_minis = FashionMini.objects.raw('SELECT * FROM main_fashionmini LIMIT 2')
    hot = Hot.objects.last()
    reviews = Review.objects.all()
    promos_width = str(100 / (promos.count() + 1))
    products = Product.objects.raw('SELECT * FROM main_product LIMIT 6')
    return render(request, 'red/index.html',
                  {'title': 'RED | Home Page', 'phone': phone_number, 'phone_ed': phone_number_ed, 'promos': promos,
                   'promos_width': promos_width, 'fashions': fashions, 'fashion_minis': fashion_minis,
                   'STATIC_URL': settings.STATIC_URL, 'hot': hot, 'reviews': reviews, 'facebook': facebook,
                   'twitter': twitter, 'linkedIn': linkedIn, 'pinterest': pinterest, 'products': products,
                   'categories': categories})


def CartView(request):
    return render(request, 'red/cart.html', {'title': 'RED | Cart', 'phone': phone_number,
                                             'phone_ed': phone_number_ed, 'categories': categories})


def ProdDetailsView(request):
    return render(request, 'red/product-details.html', {'title': 'RED | Product Details', 'phone': phone_number,
                                                        'phone_ed': phone_number_ed, 'categories': categories})


def CheckoutView(request):
    return render(request, 'red/checkout.html', {'title': 'RED | Checkout Page', 'phone': phone_number,
                                                 'phone_ed': phone_number_ed, 'categories': categories})


def ShopView(request):
    types = request.path.split('/')
    if len(types) == 2:
        types += [None, None]
    elif len(types) == 3:
        types.append(None)
    return render(request, 'red/shop.html', {'title': 'RED | Shop', 'phone': phone_number,
                                             'phone_ed': phone_number_ed,
                                             'type': types[2],
                                             'subtype': types[3], 'categories': categories})
