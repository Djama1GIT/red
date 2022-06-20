from django.shortcuts import render
from django.conf import settings
from .models import *
import json

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
    for prod in products:
        for k, v in json.loads(prod.image).items():
            prod.image = k + "/" + v[0]
    return render(request, 'red/index.html',
                  {'title': 'RED | Home Page', 'phone': phone_number, 'phone_ed': phone_number_ed, 'promos': promos,
                   'promos_width': promos_width, 'fashions': fashions, 'fashion_minis': fashion_minis,
                   'STATIC_URL': settings.STATIC_URL, 'hot': hot, 'reviews': reviews, 'facebook': facebook,
                   'twitter': twitter, 'linkedIn': linkedIn, 'pinterest': pinterest, 'products': products,
                   'categories': categories})


def CartView(request):
    return render(request, 'red/cart.html',
                  {'title': 'RED | Cart', 'phone': phone_number,
                   'phone_ed': phone_number_ed, 'categories': categories})


def ProdDetailsView(request):
    if 'id' in request.GET:
        product = Product.objects.raw('SELECT * FROM main_product WHERE id = ' + str(request.GET['id']))[0]
        product.sizes = json.loads(product.sizes)
        print(product.sizes)
        product.count = 0
        try:
            for k, v in product.sizes.items():
                product.count += v
            product.image = json.loads(product.image)
            # BETTER USE JSON!!!!!!!!!!!!!!!!!!!!!!!
            product.related = Product.objects.raw(
                'SELECT * FROM main_product WHERE (type = "' + product.type +
                '" and subtype = "' + product.subtype + '" and id != ' + str(product.id) + ') LIMIT 5')
            for prod in product.related:
                for k, v in json.loads(prod.image).items():
                    prod.image = k + "/" + v[0]
        except Exception as exc:
            return render(request, 'red/500.html')
    else:
        return render(request, 'red/404.html')
    return render(request, 'red/product-details.html',
                  {'title': 'RED | Product Details', 'phone': phone_number, 'product': product,
                   'phone_ed': phone_number_ed, 'categories': categories, 'STATIC_URL': settings.STATIC_URL})


def CheckoutView(request):
    return render(request, 'red/checkout.html',
                  {'title': 'RED | Checkout Page', 'phone': phone_number, 'phone_ed': phone_number_ed,
                   'categories': categories})


def ShopView(request):
    types = request.path.split('/')
    if len(types) == 2:
        types += [None, None]
    elif len(types) == 3:
        types += [None]
    colors = {}
    colors_tmp = Product.objects.raw(
        "SELECT distinct color, count(color) as count, id FROM main_product group by color")  # не работает distinct, возможно из-за lite sql
    for i in colors_tmp:
        colors[i.color] = i.count
    sizes = ["XS", "S", "M", "L", "XL", "XXL"]
    max_price = Product.objects.raw("SELECT max(price) as max, id from main_product")[0].max
    return render(request, 'red/shop.html',
                  {'title': 'RED | Shop', 'phone': phone_number, 'phone_ed': phone_number_ed, 'type': types[2],
                   'subtype': types[3], 'categories': categories, 'max_price': max_price,
                   'colors': colors, "sizes": sizes})


def err404(request, exception):
    return render(request, 'red/404.html', status=404)
