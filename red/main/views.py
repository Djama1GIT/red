from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.cache import cache
from django.db.models import Q
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Product, Promo, User, Review, Fashion, FashionMini, Hot, MailingList, \
    Purchase, EmailVerification
from .forms import EmailPostForm, SignUpForm, AddToCartForm, CheckoutForm, SettingsForm, UploadImageForm
from .utils import DefaultMixin, RequestInFormMixin, AnonymousRequiredMixin

import json


class ChangePhotoView(DefaultMixin, FormView):
    form_class = UploadImageForm
    template_name = 'admin/change-photo.html'
    title = 'RED | Edit'
    success_url = '/admin'

    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        model = kwargs['model']
        if request.user.is_superuser:
            prod = self.get_prod()
            if model == 'product':
                if 'delete' in request.GET:
                    images = json.loads(prod.image)
                    for k, v in images.items():
                        del images[k][int(request.GET['delete'])]
                        if len(images[k]) == 0:
                            images = '{"img/product-img": ["default.png"]}'
                            break
                    prod.image = str(images).replace("'", '"')
                    prod.save()
                    return HttpResponseRedirect(request.path)
                prod.image = json.loads(prod.image)
            else:
                if 'delete' in request.GET:
                    prod.image = 'img/product-img/default-review.png'
                    prod.save()
                    return HttpResponseRedirect(request.path)
                prod.image = json.loads('{"img/product-img": ["' + prod.image.split('/')[-1] + '"]}')
            self.extra_context = {'prod': prod, 'model': model, 'slug': slug}
        else:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['prod'] = self.get_prod()
        kwargs['model'] = self.kwargs.get('model')
        return kwargs

    def get_prod(self):
        try:
            model = self.kwargs['model']
            slug = self.kwargs['slug']
            models = {
                'product': Product,
                'review': Review,
                'fashion': Fashion,
                'fashionmini': FashionMini,
                'hot': Hot
            }
            return models[model].objects.filter(**({'id': int(slug)} if model != 'product' else {'slug': slug}))[0]
        except Exception as exc:
            print(exc)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.request.path)


class MyLoginView(DefaultMixin, LoginView):
    next_page = 'index'
    template_name = "registration/login.html"
    title = 'RED | Login'
    redirect_authenticated_user = reverse_lazy('index')


class MyLogoutView(LogoutView):
    next_page = 'index'


class SignUpView(DefaultMixin, AnonymousRequiredMixin, RequestInFormMixin, FormView, TemplateView):
    template_name = 'registration/signup.html'
    title = 'RED | Sign Up'
    form_class = SignUpForm
    success_url = reverse_lazy('signup')


class EmailVerificationView(DefaultMixin, TemplateView):
    title = 'RED | Email Verification'
    template_name = 'registration/email_verification.html'
    extra_context = {}

    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(email=kwargs.get('email'))
        _user = User.objects.get(user=user)
        email_verifications = EmailVerification.objects.filter(user=user, code=kwargs.get('code'))
        if email_verifications.exists():
            if email_verifications.first().is_expired():
                self.extra_context['message'] = 'The link has expired.'
            elif _user.is_verified_email:
                self.extra_context['message'] = 'The link is invalid.'
            else:
                _user.is_verified_email = True
                _user.save()
                self.extra_context['message'] = 'Your account has been successfully verified!'
        else:
            return HttpResponseRedirect('/')
        return super().get(request, *args, **kwargs)


class MainView(DefaultMixin, TemplateView):
    title = 'RED | Home Page'
    template_name = 'red/index.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            'promos': (promos := cache.get_or_set("main-promos", Promo.objects.filter(access="all"), 30)),
            'fashions': cache.get_or_set("main-fashions", Fashion.objects.all(), 30),
            'fashion_minis': cache.get_or_set("main-minis", FashionMini.objects.order_by('id')[:2], 30),
            'hot': cache.get_or_set("main-hot", Hot.objects.last(), 30),
            'reviews': cache.get_or_set("main-reviews", Review.objects.all(), 30),
            'promos_width': str(100 / (promos.count() + 1))
        }


class CartView(DefaultMixin, LoginRequiredMixin, TemplateView):
    template_name = 'red/cart.html'
    title = 'RED | Cart'

    def get(self, request, *args, **kwargs):
        if request.GET.get('clear') == "True" and request.user.username:
            User.objects.filter(user=request.user.id).update(cart="{}")
            return HttpResponseRedirect(reverse_lazy('cart'))
        return super().get(request, *args, **kwargs)


class ProdDetailsView(DefaultMixin, RequestInFormMixin, FormView, DetailView):
    title = 'RED | '
    template_name = 'red/product-details.html'
    form_class = AddToCartForm
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('shop')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        product = self.get_object()
        product.sizes = json.loads(product.sizes)
        form.fields['size'].choices = list(zip(map(str, range(len(product.sizes))), product.sizes.keys()))
        self.request.product_id = product.id
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        product.count = 0
        product.sizes = json.loads(product.sizes)
        sizes = dict(product.sizes)
        for k, v in sizes.items():
            if v == 0:
                del product.sizes[k]
                continue
            product.count += int(v)
        product.image = json.loads(product.image)
        product.related = cache.get_or_set(f"{self.kwargs['slug']}-{product.type}-{product.subtype}",
                                           Product.objects.filter(~Q(slug=self.kwargs['slug']), type=product.type,
                                                                  subtype=product.subtype)[:5], 30)
        for prod in product.related:
            for k, v in json.loads(prod.image).items():
                prod.image = k + "/" + v[0]
        return context | {'product': product}


class CheckoutView(DefaultMixin, RequestInFormMixin, LoginRequiredMixin, FormView):
    form_class = CheckoutForm
    template_name = 'red/checkout.html'
    title = 'RED | Checkout'
    success_url = reverse_lazy('shop')
    login_url = reverse_lazy('login')
    redirect_field_name = ''


class PurchasesView(DefaultMixin, TemplateView):
    template_name = 'red/purchases.html'
    title = 'RED | Purchases'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            'purchases': Purchase.objects.filter(user=self.request.user.id)[::-1]
        }


class SubscribeView(DefaultMixin, TemplateView):
    template_name = 'red/subscribe.html'
    title = 'RED | Subscribing'

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('mail').strip():
            if len(MailingList.objects.filter(mail=self.request.GET.get('mail'))) == 0:
                MailingList(mail=self.request.GET.get('mail')).save()
        return super().get(request, *args, **kwargs)


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
            for folder, images in json.loads(prod.image).items():
                prod.image = folder + "/" + images[0]
        return queryset


class ContactView(FormView):
    template_name = 'red/contact.html'
    form_class = EmailPostForm
    success_url = '/'


class SettingsView(DefaultMixin, RequestInFormMixin, LoginRequiredMixin, FormView):
    form_class = SettingsForm
    title = 'RED | Settings'
    template_name = 'red/settings.html'
    success_url = reverse_lazy('settings')
    login_url = reverse_lazy('login')
    redirect_field_name = ''

    def get_initial(self):
        return {
            'phone': User.objects.filter(user=self.request.user.id)[0].phone,
            'email': self.request.user.email
        }


def err404(request, exception):
    return render(request, 'errors/404.html', {'title': 'RED | Error 404'}, status=exception)


def err500(request, exception):
    return render(request, 'errors/500.html', {'title': 'RED | Error 500'}, status=exception)
