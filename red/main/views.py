from django.shortcuts import render
from django.conf import settings
from .models import *
import json
import math

phone_number = SocialMedia.objects.raw('SELECT * FROM main_socialmedia where social = "Phone number"')[0].data
phone_number_ed = SocialMedia.objects.raw('SELECT * FROM main_socialmedia where social = "Phone number ed"')[0].data
twitter = SocialMedia.objects.raw('SELECT * FROM main_socialmedia where social = "Twitter"')[0].data
facebook = SocialMedia.objects.raw('SELECT * FROM main_socialmedia where social = "Facebook"')[0].data
linkedIn = SocialMedia.objects.raw('SELECT * FROM main_socialmedia where social = "LinkedIn"')[0].data
pinterest = SocialMedia.objects.raw('SELECT * FROM main_socialmedia where social = "Pinterest"')[0].data

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


def ProdDetailsView(request, slug=None):
    if slug == None:
        return err404(request, 404)
    try:
        product = Product.objects.raw('SELECT * FROM main_product WHERE slug = "' + slug + '"')[0]
    except Exception:
        return err404(request, 404)
    product.sizes = json.loads(product.sizes)
    product.count = 0
    try:
        for k, v in product.sizes.items():
            product.count += v
        product.image = json.loads(product.image)
        # BETTER USE JSON!!!!!!!!!!!!!!!!!!!!!!!
        product.related = Product.objects.raw(
            'SELECT id, image, price, name FROM main_product WHERE (type = "' + product.type +
            '" and subtype = "' + product.subtype + '" and slug != "' + product.slug + '") LIMIT 5')
        for prod in product.related:
            for k, v in json.loads(prod.image).items():
                prod.image = k + "/" + v[0]
    except Exception as exc:
        return render(request, 'red/500.html')
    return render(request, 'red/product-details.html',
                  {'title': 'RED | Product Details', 'phone': phone_number, 'product': product,
                   'phone_ed': phone_number_ed, 'categories': categories, 'STATIC_URL': settings.STATIC_URL})


def CheckoutView(request):
    return render(request, 'red/checkout.html',
                  {'title': 'RED | Checkout Page', 'phone': phone_number, 'phone_ed': phone_number_ed,
                   'categories': categories})


def ShopView(request, cat=None, subcat=None):
    where = ""
    if cat:
        where += f"WHERE type = '{cat}'"
        if subcat:
            where += f" and subtype = '{subcat}' "
    request_where = where[:]
    if 'size' in request.GET:
        if "WHERE " in where:
            where += " and "
        else:
            where += "WHERE "
        where += f'(sizes like \'%"{request.GET["size"]}"%\' or sizes like "%\'{request.GET["size"]}\'%")'
    if 'color' in request.GET:
        if "WHERE " in where:
            where += " and "
        else:
            where += "WHERE "
        where += f'color = "{request.GET["color"]}"'
    colors = {}
    colors_tmp = Product.objects.raw(
        f"SELECT distinct color, count(color) as count, id FROM main_product {request_where} group by color")
    for i in colors_tmp:
        colors[i.color] = i.count
    sizes = ["XS", "S", "M", "L", "XL", "XXL"]
    max_price = Product.objects.raw(f"SELECT max(price) as max, id from main_product {request_where}")[0].max
    products_on_page = 9
    pages = math.ceil(
        Product.objects.raw(f"SELECT id, count(*) as count from main_product {where}")[0].count / products_on_page)
    active_page = int(request.GET['page']) if 'page' in request.GET else 1
    if active_page > pages:
        active_page = 1
    products = Product.objects.raw(
        f"SELECT id, name, price, image, type, subtype from main_product {where}LIMIT "
        f"{active_page * products_on_page - products_on_page},{products_on_page}")
    for prod in products:
        for k, v in json.loads(prod.image).items():
            prod.image = k + "/" + v[0]
    return render(request, 'red/shop.html',
                  {'title': 'RED | Shop', 'phone': phone_number, 'phone_ed': phone_number_ed, 'type': cat,
                   'subtype': subcat, 'categories': categories, 'max_price': max_price,
                   'colors': colors, 'sizes': sizes, 'pages': range(1, pages + 1), 'active_page': active_page,
                   'products': products, 'STATIC_URL': settings.STATIC_URL})


def err404(request, exception):
    return render(request, 'red/404.html',
                  {'title': 'RED | Home Page', 'phone': phone_number, 'phone_ed': phone_number_ed,
                   'STATIC_URL': settings.STATIC_URL, 'facebook': facebook, 'twitter': twitter, 'linkedIn': linkedIn,
                   'pinterest': pinterest, 'categories': categories}, status=404
                  )
