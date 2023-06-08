from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.cache import cache
from django.db.models import Q
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.contrib.auth import views as auth_views, authenticate, get_user_model
from django.contrib.auth.models import User as user

from .models import Product, Promo, User, Review, Fashion, FashionMini, Hot, MailingList, \
    Comment, Purchase, UploadImage, EmailVerification
from .forms import EmailPostForm, SignUpForm, AddToCartForm, CheckoutForm, SettingsForm, UploadImageForm
from .tasks import send_email_verification
from .utils import DefaultMixin
from .context_processors import cart

import json


class myLoginView(auth_views.LoginView):
    next_page = 'index'
    template_name = "registration/login.html"
    extra_context = {'title': 'RED | Login'}


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
                           'what': what})
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
                      {'title': 'RED | Sign Up', 'form': form})

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
                            send_email_verification.delay(up_user.id)
                            return HttpResponseRedirect('/Login/')
                        else:
                            raise Exception('Database error')
        else:
            print(form.cleaned_data, form.errors)
        return render(request, 'registration/signup.html',
                      {'title': 'RED | Home Page', 'form': form})

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


class EmailVerificationView(View):
    def get(self, request, email, code):
        user = get_user_model().objects.get(email=email)
        _user = User.objects.get(user=user)
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists():
            if email_verifications.first().is_expired():
                message = 'Срок действия ссылки истек.'
            elif _user.is_verified_email:
                message = 'Ссылка недействительна.'
                print(message)
            else:
                _user.is_verified_email = True
                _user.save()
                message = 'Ваша учетная запись успешно подтверждена!'
                print(message)
        else:
            return HttpResponseRedirect('/')
        return render(request, 'registration/email_verification.html',
                      {'title': 'RED | Email Verification',
                       'message': message})


def MainView(request):
    promos = cache.get_or_set("main-promos", Promo.objects.filter(access="all"), 30)
    fashions = cache.get_or_set("main-fashions", Fashion.objects.all(), 30)
    fashion_minis = cache.get_or_set("main-minis", FashionMini.objects.order_by('id')[:2], 30)
    hot = cache.get_or_set("main-hot", Hot.objects.last(), 30)
    reviews = cache.get_or_set("main-reviews", Review.objects.all(), 30)
    promos_width = str(100 / (promos.count() + 1))
    products = cache.get_or_set("main-prods", Product.objects.order_by('-id')[:6], 30)
    for prod in products:
        for k, v in json.loads(prod.image).items():
            prod.image = k + "/" + v[0]
    return render(request, 'red/index.html',
                  {'title': 'RED | Home Page', 'promos': promos,
                   'promos_width': promos_width, 'fashions': fashions, 'fashion_minis': fashion_minis,
                   'hot': hot, 'reviews': reviews})


def CartView(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/')
    if "clear" in request.GET:
        if request.GET["clear"] == "True" and request.user.username:
            User.objects.filter(user=request.user.id).update(cart="{}")
            return HttpResponseRedirect('/Cart/')
    return render(request, 'red/cart.html',
                  {'title': 'RED | Cart'})


def ProdDetailsView(request, slug=None):
    if slug == None:
        return err404(request, 404)
    try:
        product = cache.get_or_set(slug, Product.objects.filter(slug=slug)[0], 30)
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
        product.related = cache.get_or_set(f"{slug}-{product.type}-{product.subtype}",
                                           Product.objects.filter(~Q(slug=slug), type=product.type,
                                                                  subtype=product.subtype)[:5], 30)
        for prod in product.related:
            for k, v in json.loads(prod.image).items():
                prod.image = k + "/" + v[0]
    except Exception as exc:
        return render(request, 'errors/500.html')
    sizes = list(zip(map(str, range(len(product.sizes))), product.sizes.keys()))
    form = AddToCartForm(request.POST, sizes)
    if 'addtocart' in request.POST:
        if request.user.is_anonymous:
            return HttpResponseRedirect('/Login')
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
                  {'form': form, 'title': 'RED | ', 'product': product})


def CheckoutView(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/')
    form = CheckoutForm(request.POST)
    cat = cart(request)['cart']
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
                  {'form': form, 'title': 'RED | Checkout Page'})


class PurchasesView(DefaultMixin, TemplateView):
    template_name = 'red/purchases.html'
    title = 'RED | Purchases'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchases'] = Purchase.objects.filter(user=self.request.user.id)[::-1]
        return context


class SubscribeView(DefaultMixin, TemplateView):
    template_name = 'red/subscribe.html'
    title = 'RED | Subscribing'

    def get_context_data(self, **kwargs):
        if "mail" in self.request.GET:
            if self.request.GET["mail"].strip() != "":
                if len(MailingList.objects.filter(mail=self.request.GET["mail"])) == 0:
                    MailingList(mail=self.request.GET["mail"]).save()


class ShopListView(DefaultMixin, ListView):
    model = Product
    template_name = 'red/shop.html'
    paginate_by = 6
    title = 'RED | Shop'

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.kwargs.copy()

        if color := self.request.GET.get('color'):
            params['color'] = color
        if size := self.request.GET.get('size'):
            params['sizes__contains'] = size

        queryset = queryset.filter(**params)

        for prod in queryset:
            for k, v in json.loads(prod.image).items():
                prod.image = k + "/" + v[0]
        return queryset


class ContactView(FormView):
    template_name = 'red/contact.html'
    form_class = EmailPostForm
    success_url = '/'

    def form_valid(self, form):
        Comment(name=form.cleaned_data["name"], lastname=form.cleaned_data["lastname"],
                mail=form.cleaned_data["email"], comment=form.cleaned_data["comment"]).save()
        return super().form_valid(form)


class SettingsView(View):
    def get(self, request):
        if request.user.is_anonymous:
            return HttpResponseRedirect('/')
        form = SettingsForm(
            initial={'phone': User.objects.filter(user=request.user.id)[0].phone, 'mail': request.user.email})
        return render(request, 'red/settings.html',
                      {'form': form, 'title': 'RED | Settings'})

    def post(self, request):
        global form
        if request.user.is_anonymous:
            return HttpResponseRedirect('/')
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
                          {'form': form, 'title': 'RED | Settings'})

    def check_password(self, password: str, repeat_password: str, username: str):
        if password == repeat_password and len(password) >= 8 and (
                not password.isnumeric()) and username != password:
            return True
        else:
            form.add_error('passwd', 'Invalid password')
            return False


def err404(request, exception):
    return render(request, 'errors/404.html', {'title': 'RED | Error 404'}, status=exception)


def err500(request, exception):
    return render(request, 'errors/500.html', {'title': 'RED | Error 500'}, status=exception)
