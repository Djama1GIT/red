import random

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.db.models import Q
from django.views import View
from django.contrib.auth import views as auth_views, authenticate
from django.contrib.auth.models import User as user
from .models import Product, Promo, User, Review, Fashion, FashionMini, Hot, Category, SocialMedia, MailingList, \
    Comment, Purchase, UploadImage
from .forms import EmailPostForm, SignUpForm, AddToCartForm, CheckoutForm, SettingsForm, UploadImageForm

import json
import math

phone_number = SocialMedia.objects.filter(social='Phone number')[0].data
phone_number_ed = SocialMedia.objects.filter(social='Phone number ed')[0].data
twitter = SocialMedia.objects.filter(social='Twitter')[0].data
facebook = SocialMedia.objects.filter(social='Facebook')[0].data
linkedIn = SocialMedia.objects.filter(social='LinkedIn')[0].data
pinterest = SocialMedia.objects.filter(social='Pinterest')[0].data
products_on_page = 6

categories = {}
for i in Category.objects.order_by('id').iterator():
    if i.type in categories:
        if i.subtype != "None":
            categories[i.type] += [i.subtype]
    else:
        categories[i.type] = []

extra = {'phone': phone_number, 'phone_ed': phone_number_ed,
         'STATIC_URL': settings.STATIC_URL, 'facebook': facebook, 'twitter': twitter, 'linkedIn': linkedIn,
         'pinterest': pinterest, 'categories': categories}


def cart(request):
    if request.user.is_anonymous:
        return None
    cat = User.objects.filter(user=request.user.id)[0].cart
    cat = json.loads(cat)
    _cart_ = {}
    cart_sum = 0
    for k, v in cat.items():
        product = Product.objects.filter(id=int(k))[0]
        sizes = dict(json.loads(product.sizes))
        count_sizes = 0
        if v in sizes.keys():
            count_sizes = sizes[v]
        for z, a in json.loads(product.image).items():
            product.image = z + "/" + a[0]
        if count_sizes > 0:
            cart_sum += product.price
        _cart_[product.name] = [product.price, product.image, product.slug, v, count_sizes, 1 if count_sizes > 1 else 0]
    cart_sum = float('{:.2f}'.format(cart_sum))
    return [_cart_, cart_sum]


class myLoginView(auth_views.LoginView):
    next_page = 'index'
    template_name = "registration/login.html"
    extra_context = {'title': 'RED | Login'} | extra


class myLogoutView(auth_views.LogoutView):
    next_page = 'index'


class ChangePhotoView(View):
    prod = None

    def get(self, request, what, slug):
        if request.user.is_superuser:
            if what == 'product':
                try:
                    self.prod = Product.objects.filter(slug=slug)[0]
                    if 'delete' in request.GET:
                        images = json.loads(self.prod.image)
                        for k, v in images.items():
                            del images[k][int(request.GET['delete'])]
                            if len(images[k]) == 0:
                                images = '{"img/product-img": ["default.png"]}'
                                break
                        images = str(images)
                        self.prod.image = images.replace("'", '"')
                        self.prod.save()
                        return HttpResponseRedirect(request.path)
                    self.prod.image = json.loads(self.prod.image)
                except Exception:
                    return HttpResponseRedirect('/admin/main')
            elif what == 'review':
                try:
                    self.prod = Review.objects.filter(id=int(slug))[0]
                    self.prod.image = '{"img/product-img": ["' + self.prod.image.split('/')[-1] + '"]}'
                    if 'delete' in request.GET:
                        self.prod.image = 'img/product-img/default-review.png'
                        self.prod.save()
                        return HttpResponseRedirect(request.path)
                    self.prod.image = json.loads(self.prod.image)
                except Exception:
                    return HttpResponseRedirect('/admin/main')
            elif what == 'fashion':
                try:
                    self.prod = Fashion.objects.filter(id=int(slug))[0]
                    self.prod.image = '{"img/product-img": ["' + self.prod.image.split('/')[-1] + '"]}'
                    if 'delete' in request.GET:
                        self.prod.image = 'img/product-img/default-review.png'
                        self.prod.save()
                        return HttpResponseRedirect(request.path)
                    self.prod.image = json.loads(self.prod.image)
                except Exception:
                    return HttpResponseRedirect('/admin/main')
            elif what == 'fashionmini':
                try:
                    self.prod = FashionMini.objects.filter(id=int(slug))[0]
                    self.prod.image = '{"img/product-img": ["' + self.prod.image.split('/')[-1] + '"]}'
                    if 'delete' in request.GET:
                        self.prod.image = 'img/product-img/default-review.png'
                        self.prod.save()
                        return HttpResponseRedirect(request.path)
                    self.prod.image = json.loads(self.prod.image)
                except Exception:
                    return HttpResponseRedirect('/admin/main')
            elif what == 'hot':
                try:
                    self.prod = Hot.objects.filter(id=int(slug))[0]
                    self.prod.image = '{"img/product-img": ["' + self.prod.image.split('/')[-1] + '"]}'
                    if 'delete' in request.GET:
                        self.prod.image = 'img/product-img/default-review.png'
                        self.prod.save()
                        return HttpResponseRedirect(request.path)
                    self.prod.image = json.loads(self.prod.image)
                except Exception:
                    return HttpResponseRedirect('/admin/main')
            else:
                return HttpResponseRedirect('/admin/main')
            form = UploadImageForm()
            return render(request, 'admin/change-photo.html',
                          {'form': form, 'slug': slug, 'title': 'RED | Sign Up', 'prod': self.prod,
                           'what': what} | extra)
        else:
            return HttpResponseRedirect('/')

    def post(self, request, what, slug, *args, **kwargs):
        form = UploadImageForm(request.POST, request.FILES)
        if what == "product":
            try:
                self.prod = Product.objects.filter(slug=slug)[0]
            except Exception:
                return HttpResponseRedirect('/admin/main')
        elif what == 'fashion':
            try:
                self.prod = Fashion.objects.filter(id=int(slug))[0]
            except Exception:
                return HttpResponseRedirect('/admin/main')
        elif what == 'fashionmini':
            try:
                self.prod = FashionMini.objects.filter(id=int(slug))[0]
            except Exception:
                return HttpResponseRedirect('/admin/main')
        elif what == 'hot':
            try:
                self.prod = Hot.objects.filter(id=int(slug))[0]
            except Exception:
                return HttpResponseRedirect('/admin/main')
        elif what == 'review':
            try:
                self.prod = Review.objects.filter(id=int(slug))[0]
            except Exception:
                return HttpResponseRedirect('/admin/main')
        else:
            return HttpResponseRedirect('/admin/main')
        if form.is_valid():
            if what == "product":
                images = json.loads(self.prod.image)
                images['img/product-img'] += [self.upload(form).split('/')[-1]]
                images = str(images)
                self.prod.image = images.replace("'", '"')
            elif what in ["review", "fashion", "fashionmini", "hot"]:
                self.prod.image = 'img/product-img/' + self.upload(form).split('/')[-1]
            self.prod.save()
        return HttpResponseRedirect(request.path)

    def upload(self, form):
        img = form.cleaned_data["image"]
        obj = UploadImage(img=img)
        obj.save()
        return str(obj.img)


class SignUpView(View):
    def get(self, request):
        if request.user.id:
            return HttpResponseRedirect('/')
        form = SignUpForm()
        return render(request, 'registration/signup.html',
                      {'title': 'RED | Sign Up', 'form': form} | extra)

    def post(self, request):
        global form
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            keys = data.keys()
            if "login" in keys and "passwd" in keys and "repeat_passwd" in keys and "mail" in keys and "phone" in keys:
                if not user.objects.filter(username=data["login"]):
                    if self.check_username(data["login"]) and self.check_password(data["passwd"], data["repeat_passwd"],
                                                                                  data["login"]):
                        user.objects.create_user(username=data["login"],
                                                 email=data["mail"],
                                                 password=data["passwd"])
                        up_user = authenticate(request, username=data["login"], password=data["passwd"])
                        User(user_login=up_user, user=up_user, phone=data["phone"]).save()
                        if up_user is not None:
                            return HttpResponseRedirect('/Login/')
                        else:
                            raise Exception('Database error')
        else:
            print(form.cleaned_data, form.errors)
        return render(request, 'registration/signup.html',
                      {'cart': cart(request), 'title': 'RED | Home Page', 'form': form} | extra)

    def check_username(self, username: str):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890@.+-_"
        for symbol in username:
            if symbol in alphabet:
                continue
            else:
                form.add_error('login', 'Invalid username')
                return False
        else:
            return True

    def check_password(self, password: str, repeat_password: str, username: str):
        if password == repeat_password and len(password) >= 8 and (
                not password.isnumeric()) and username != password:
            return True
        else:
            form.add_error('passwd', 'Invalid password')
            return False


def MainView(request):
    promos = Promo.objects.filter(access="all")
    fashions = Fashion.objects.all()
    fashion_minis = FashionMini.objects.order_by('id')[:2]
    hot = Hot.objects.last()
    reviews = Review.objects.all()
    promos_width = str(100 / (promos.count() + 1))
    products = Product.objects.order_by('-id')[:6]
    for prod in products:
        for k, v in json.loads(prod.image).items():
            prod.image = k + "/" + v[0]
    return render(request, 'red/index.html',
                  {'cart': cart(request), 'title': 'RED | Home Page', 'promos': promos,
                   'promos_width': promos_width, 'fashions': fashions, 'fashion_minis': fashion_minis,
                   'hot': hot, 'reviews': reviews} | extra)


def CartView(request):
    if "clear" in request.GET:
        if request.GET["clear"] == "True" and request.user.username:
            User.objects.filter(user=request.user.id).update(cart="{}")
            return HttpResponseRedirect('/Cart/')

    return render(request, 'red/cart.html',
                  {'cart': cart(request), 'title': 'RED | Cart'} | extra)


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
        x = dict(product.sizes)
        for k, v in x.items():
            if v == 0:
                del product.sizes[k]
                continue
            product.count += int(v)
        product.image = json.loads(product.image)
        product.related = Product.objects.filter(~Q(slug=slug), type=product.type, subtype=product.subtype)[:5]
        for prod in product.related:
            for k, v in json.loads(prod.image).items():
                prod.image = k + "/" + v[0]
    except Exception as exc:
        return render(request, 'errors/500.html')
    sizes = list(zip(map(str, range(len(product.sizes))), product.sizes.keys()))
    form = AddToCartForm(request.POST, sizes)
    if 'addtocart' in request.POST:
        if form.is_valid():
            data = form.cleaned_data
            bd = User.objects.filter(user=request.user.id)[0].cart
            load = json.loads(bd)
            load.update({str(product.id): list(product.sizes.keys())[int(data['size'])]})
            dump = json.dumps(load)
            User.objects.filter(user=request.user.id).update(
                cart=dump)
            HttpResponseRedirect(request.get_full_path())
    return render(request, 'red/product-details.html',
                  {'form': form, 'cart': cart(request), 'title': 'RED | ', 'product': product} | extra)


def CheckoutView(request):
    form = CheckoutForm(request.POST)
    cat = cart(request)
    if cat[0]:
        if form.is_valid():
            data = form.cleaned_data
            for k, v in cat[0].items():
                new_sizes = json.loads(Product.objects.filter(slug=v[2])[0].sizes)
                if v[3] in new_sizes:
                    if new_sizes[v[3]] > 0:
                        Purchase(user_login=request.user.username, user=request.user, first_name=data['first_name'],
                                 last_name=data['last_name'], country=data['country'], address=data['address'],
                                 postcode=data['postcode'], city=data['city'], province=data['province'],
                                 product=k, size=v[3], price=v[0], slug=v[2], image=v[1]).save()
                        new_sizes[v[3]] -= 1
                        Product.objects.filter(slug=v[2]).update(sizes=json.dumps(new_sizes))
            User.objects.filter(user=request.user.id).update(cart="{}")
            return HttpResponseRedirect('/Shop/')
    else:
        return HttpResponseRedirect('/Purchases/')
    return render(request, 'red/checkout.html',
                  {'form': form, 'cart': cat, 'title': 'RED | Checkout Page'} | extra)


def PurchasesView(request):
    purchases = Purchase.objects.filter(user=request.user.id)[::-1]
    return render(request, 'red/purchases.html',
                  {'purchases': purchases, 'cart': cart(request), 'title': 'RED | Purchases'} | extra)


def SubsribeView(request):
    if "mail" in request.GET:
        if request.GET["mail"].strip() != "":
            if len(MailingList.objects.filter(mail=request.GET["mail"])) == 0:
                MailingList(mail=request.GET["mail"]).save()

    return render(request, 'red/subscribe.html',
                  {'cart': cart(request), 'title': 'RED | Subscribing'} | extra)


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
    pages = math.ceil(
        Product.objects.raw(f"SELECT 1 as id, count(*) as count from main_product {where}")[0].count / products_on_page)
    active_page = int(request.GET['page']) if 'page' in request.GET else 1
    if active_page > pages:
        active_page = 1
    products = Product.objects.raw(
        f"SELECT id, name, price, image, type, subtype from main_product {where} ORDER BY -id LIMIT "
        f"{products_on_page} OFFSET {active_page * products_on_page - products_on_page}")
    for prod in products:
        for k, v in json.loads(prod.image).items():
            prod.image = k + "/" + v[0]
    return render(request, 'red/shop.html',
                  {'cart': cart(request), 'title': 'RED | Shop', 'type': cat,
                   'subtype': subcat, 'colors': colors, 'sizes': sizes,
                   'pages': range(1, pages + 1), 'active_page': active_page,
                   'products': products} | extra)


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
                  {'cart': cart(request), 'form': form, 'title': 'RED | Contact'} | extra)


class SettingsView(View):
    def get(self, request):
        form = SettingsForm(
            initial={'phone': User.objects.filter(user=request.user.id)[0].phone, 'mail': request.user.email})
        return render(request, 'red/settings.html',
                      {'cart': cart(request), 'form': form, 'title': 'RED | Settings'} | extra)

    def post(self, request):
        global form
        red = False
        form = SettingsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if (data['mail'] != user.objects.filter(username=request.user.username)[0].email) and data['mail']:
                red = True
                user.objects.filter(username=request.user.username).update(email=data['mail'])
            if (data['phone'] != int(User.objects.filter(user=request.user.id)[0].phone)) and data['phone']:
                red = True
                User.objects.filter(user=request.user.id).update(phone=data['phone'])
            if data['old']:
                au = authenticate(request, username=request.user.username, password=data["old"])
                if au:
                    if self.check_password(data['passwd'], data['repeat_passwd'], request.user.username):
                        s = user.objects.get(username=request.user.username)
                        s.set_password(str(data['passwd'].strip()))
                        s.save()
                        return HttpResponseRedirect('/Login/')
                else:
                    form.add_error('old', 'Incorrect password')
        if red:
            return HttpResponseRedirect(request.get_full_path())
        else:
            return render(request, 'red/settings.html',
                          {'cart': cart(request), 'form': form, 'title': 'RED | Settings'} | extra)

    def check_password(self, password: str, repeat_password: str, username: str):
        if password == repeat_password and len(password) >= 8 and (
                not password.isnumeric()) and username != password:
            return True
        else:
            form.add_error('passwd', 'Invalid password')
            return False


def err404(request, exception):
    return render(request, 'errors/404.html',
                  {'cart': cart(request), 'title': 'RED | Error 404'} | extra, status=exception
                  )


def err500(request, exception):
    return render(request, 'errors/500.html',
                  {'cart': cart(request), 'title': 'RED | Error 500'} | extra, status=exception
                  )
