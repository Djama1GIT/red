from django.shortcuts import render
from django.conf import settings
from .models import *

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
        prod.image = prod.image[:prod.image.find(':')] + "/" + prod.image[prod.image.find(':')+1:prod.image.find(',')]
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
        product.sizes = product.sizes.split()
        x = {}
        product.count = 0
        try:
            for i in product.sizes:
                size = i.split(':')
                count = int(size[1])
                if count > 0:
                    product.count += count
                    x[size[0]] = count
            product.sizes = x
            product.image = product.image.split(';')
            images = {}
            for imags in product.image:
                imgs = imags.split(':')
                images[imgs[0]] = imgs[1].split(',')
            product.image = images
            # BETTER USE JSON!!!!!!!!!!!!!!!!!!!!!!!
            product.related = Product.objects.raw(
                'SELECT * FROM main_product WHERE (type = "' + product.type +
                '" and subtype = "' + product.subtype + '" and id != ' + str(product.id) + ') LIMIT 5')
            for prod in product.related:
                prod.image = prod.image[:prod.image.find(':')] + "/" + \
                             prod.image[prod.image.find(':')+1:prod.image.find(',')]
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
        types.append(None)
    return render(request, 'red/shop.html',
                  {'title': 'RED | Shop', 'phone': phone_number, 'phone_ed': phone_number_ed, 'type': types[2],
                   'subtype': types[3], 'categories': categories})


def err404(request, exception):
    return render(request, 'red/404.html', status=404)
