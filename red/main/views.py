from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.db.models import Q
from .models import *
from .forms import EmailPostForm, LogInForm, SignUpForm
import json
import math

phone_number = SocialMedia.objects.filter(social='Phone number')[0].data
phone_number_ed = SocialMedia.objects.filter(social='Phone number ed')[0].data
twitter = SocialMedia.objects.filter(social='Twitter')[0].data
facebook = SocialMedia.objects.filter(social='Facebook')[0].data
linkedIn = SocialMedia.objects.filter(social='LinkedIn')[0].data
pinterest = SocialMedia.objects.filter(social='Pinterest')[0].data

categories = {}
for i in Category.objects.order_by('id').iterator():
    print(i)
    if i.type in categories:
        if i.subtype != "None":
            categories[i.type] += [i.subtype]
    else:
        categories[i.type] = []


def MainView(request):
    promos = Promo.objects.filter(access="all")
    fashions = Fashion.objects.all()
    fashion_minis = FashionMini.objects.order_by('id')[:2]
    hot = Hot.objects.last()
    reviews = Review.objects.all()
    promos_width = str(100 / (promos.count() + 1))
    products = Product.objects.order_by('id')[:6:-1]
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
        product = Product.objects.filter(slug=slug)[0]
    except Exception:
        return err404(request, 404)
    product.sizes = json.loads(product.sizes)
    product.count = 0
    try:
        for k, v in product.sizes.items():
            product.count += v
        product.image = json.loads(product.image)
        # BETTER USE JSON!!!!!!!!!!!!!!!!!!!!!!!
        product.related = Product.objects.filter(~Q(slug=slug), type=product.type, subtype=product.subtype)[:5]
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


def LoginView(request):
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            ...
        return HttpResponseRedirect('/Shop')
    else:
        form = LogInForm()
    return render(request, 'red/login.html',
                  {'form': form, 'title': 'RED | Log In', 'phone': phone_number, 'phone_ed': phone_number_ed,
                   'categories': categories})


def SignUpView(request):
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            ...
        return HttpResponseRedirect('/Shop')
    else:
        form = SignUpForm()
    return render(request, 'red/signup.html',
                  {'form': form, 'title': 'RED | Sign Up', 'phone': phone_number, 'phone_ed': phone_number_ed,
                   'categories': categories})


def SubsribeView(request):
    if "mail" in request.GET:
        if request.GET["mail"].strip() != "":
            if len(MailingList.objects.filter(mail=request.GET["mail"])) == 0:
                MailingList(mail=request.GET["mail"]).save()

    return render(request, 'red/subscribe.html',
                  {'title': 'RED | Subscribe | Redirection..', 'phone': phone_number, 'phone_ed': phone_number_ed,
                   'categories': categories})


def ShopView(request, cat=None, subcat=None):
    where = ""
    if cat:
        where += f"WHERE type = '{cat}'"
        if subcat:
            where += f" and subtype = '{subcat}' "
    request_where = where[:]
    if 'size' in request.GET:
        where += " and " if "WHERE " in where else "WHERE "
        where += f'(sizes like \'%\'{request.GET["size"]}\'%\' or sizes like \'%\'{request.GET["size"]}\'%\')'
    if 'color' in request.GET:
        where += " and " if "WHERE " in where else "WHERE "
        where += f'color = \'{request.GET["color"]}\''
    colors = {}
    colors_tmp = Product.objects.raw(
        f"SELECT distinct color, count(color) as count, 1 as id FROM main_product {request_where} group by color")
    for i in colors_tmp:
        colors[i.color] = i.count
    sizes = ["XS", "S", "M", "L", "XL", "XXL"]
    products_on_page = 9
    pages = math.ceil(
        Product.objects.raw(f"SELECT 1 as id, count(*) as count from main_product {where}")[0].count / products_on_page)
    active_page = int(request.GET['page']) if 'page' in request.GET else 1
    if active_page > pages:
        active_page = 1
    print(active_page * products_on_page - products_on_page)
    products = Product.objects.raw(
        f"SELECT id, name, price, image, type, subtype from main_product {where} ORDER BY id LIMIT "
        f"{products_on_page} OFFSET {active_page * products_on_page - products_on_page}")[::-1]
    for prod in products:
        for k, v in json.loads(prod.image).items():
            prod.image = k + "/" + v[0]
    return render(request, 'red/shop.html',
                  {'title': 'RED | Shop', 'phone': phone_number, 'phone_ed': phone_number_ed, 'type': cat,
                   'subtype': subcat, 'categories': categories, 'colors': colors, 'sizes': sizes,
                   'pages': range(1, pages + 1), 'active_page': active_page,
                   'products': products, 'STATIC_URL': settings.STATIC_URL})


def ContactView(request):
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            Comment(name=form.cleaned_data["name"], lastname=form.cleaned_data["lastname"],
                    mail=form.cleaned_data["email"], comment=form.cleaned_data["comment"]).save()
        return HttpResponseRedirect('/')
    else:
        form = EmailPostForm()
    return render(request, 'red/contact.html',
                  {'form': form, 'title': 'RED | Home Page', 'phone': phone_number, 'phone_ed': phone_number_ed,
                   'STATIC_URL': settings.STATIC_URL, 'facebook': facebook, 'twitter': twitter, 'linkedIn': linkedIn,
                   'pinterest': pinterest, 'categories': categories})


def err404(request, exception):
    return render(request, 'red/404.html',
                  {'title': 'RED | Home Page', 'phone': phone_number, 'phone_ed': phone_number_ed,
                   'STATIC_URL': settings.STATIC_URL, 'facebook': facebook, 'twitter': twitter, 'linkedIn': linkedIn,
                   'pinterest': pinterest, 'categories': categories}, status=404
                  )
