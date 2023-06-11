from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as user
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .models import User, Product, Comment, Purchase, UploadImage
from .utils import ValidateMixin, FormWithRequestMixin
from .tasks import send_email_verification

import json


class AddToCartForm(FormWithRequestMixin, forms.Form):
    size = forms.ChoiceField(widget=forms.RadioSelect(), choices=[])
    product = forms.SlugField()

    def save(self):
        _user = User.objects.filter(user=self.request.user.id)[0].cart
        load = json.loads(_user)
        product = Product.objects.filter(id=self.request.product_id)[0]
        product.sizes = json.loads(product.sizes)
        load.update({str(product.id): list(product.sizes.keys())[int(self.data.get('size'))]})
        dump = json.dumps(load)
        User.objects.filter(user=self.request.user.id).update(cart=dump)

    def clean(self):
        self.save()
        return HttpResponseRedirect(self.request.get_full_path())


class EmailPostForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter First Name'}), max_length=48)
    lastname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name'}), max_length=48)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter Your Email'}), max_length=56)
    comment = forms.CharField(widget=forms.Textarea())

    def save(self):
        comment = Comment(name=self.cleaned_data.get("name"), lastname=self.cleaned_data.get("lastname"),
                          mail=self.cleaned_data.get("email"), comment=self.cleaned_data.get("comment"))
        comment.save()
        return comment

    def clean(self):
        cleaned_data = super().clean()
        self.save()
        return cleaned_data


class SignUpForm(FormWithRequestMixin, ValidateMixin, forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Login'}),
                            max_length=48)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
                             max_length=56)
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Phone number'}),
                               min_value=1000000000,
                               max_value=9999999999)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
                               min_length=8,
                               max_length=48)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
                                       min_length=8,
                                       max_length=48)

    def clean_login(self):
        login = self.cleaned_data.get('login')
        if user.objects.filter(username=login).exists():
            raise forms.ValidationError('This login is already taken. Please choose another.')
        if not self.check_username(login):
            raise forms.ValidationError('The username is not valid.')
        return login

    def clean(self):
        cleaned_data = super().clean()
        passwd = cleaned_data.get('password')
        repeat_passwd = cleaned_data.get('repeat_passwd')
        if passwd != repeat_passwd:
            self.add_error('confirm_password', 'Passwords do not match.')
        elif not self.check_password(passwd, repeat_passwd, cleaned_data.get('login')):
            self.add_error('confirm_password', 'Invalid Password')
        self.save()
        return cleaned_data

    def save(self):
        user_obj = user.objects.create_user(
            username=self.cleaned_data.get('login'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password')
        )
        User.objects.create(
            user_login=user_obj,
            user=user_obj,
            phone=self.cleaned_data.get('phone')
        )
        send_email_verification.delay(user_obj.id)
        return HttpResponseRedirect(reverse_lazy('login'))


class CheckoutForm(FormWithRequestMixin, forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(), max_length=48)
    last_name = forms.CharField(widget=forms.TextInput(), max_length=48)
    country = forms.CharField(widget=forms.TextInput(), max_length=48)
    address = forms.CharField(widget=forms.TextInput(), max_length=48)
    postcode = forms.CharField(widget=forms.TextInput(), max_length=48)
    city = forms.CharField(widget=forms.TextInput(), max_length=48)
    province = forms.CharField(widget=forms.TextInput(), max_length=48)

    def save(self):
        cart = json.loads(User.objects.filter(user=self.request.user.id)[0].cart)
        _cart = {}
        for id, size in cart.items():
            product = Product.objects.filter(id=int(id))[0]
            sizes = dict(json.loads(product.sizes))
            count_sizes = 0
            if size in sizes.keys():
                count_sizes = sizes[size]
            for folder, images in json.loads(product.image).items():
                product.image = folder + "/" + images[0]
            _cart[product.name] = [product.price, product.image,
                                   product.slug, size, count_sizes, 1 if count_sizes > 1 else 0]

        if _cart:
            for name, attrs in _cart.items():
                new_sizes = json.loads(Product.objects.filter(slug=attrs[2])[0].sizes)
                if attrs[3] in new_sizes:
                    if new_sizes[attrs[3]] > 0:
                        Purchase(user_login=self.request.user.username,
                                 user=self.request.user,
                                 first_name=self.data.get('first_name'),
                                 last_name=self.data.get('last_name'),
                                 country=self.data.get('country'),
                                 address=self.data.get('address'),
                                 postcode=self.data.get('postcode'),
                                 city=self.data.get('city'),
                                 province=self.data.get('province'),
                                 product=name,
                                 size=attrs[3],
                                 price=attrs[0],
                                 slug=attrs[2],
                                 image=attrs[1]).save()
                        new_sizes[attrs[3]] -= 1
                        Product.objects.filter(slug=attrs[2]).update(sizes=json.dumps(new_sizes))
            User.objects.filter(user=self.request.user.id).update(cart="{}")
            return HttpResponseRedirect(reverse_lazy('shop'))
        else:
            return HttpResponseRedirect(reverse_lazy('purchases'))

    def clean(self):
        super().clean()
        return self.save()


class SettingsForm(FormWithRequestMixin, ValidateMixin, forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}),
        max_length=56,
        required=False
    )
    phone = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Phone number'}),
        min_value=1000000000,
        max_value=9999999999,
        required=False
    )
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter old password'}),
        min_length=8,
        max_length=48,
        required=False
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
        min_length=8,
        max_length=48,
        required=False
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}),
        min_length=8,
        max_length=48,
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        self.validate_email(cleaned_data)
        self.validate_phone(cleaned_data)
        self.validate_password(cleaned_data)

    def validate_email(self, cleaned_data):
        email = cleaned_data.get('email')
        if email and email != self.request.user.email:
            user.objects.filter(username=self.request.user.username).update(email=email)

    def validate_phone(self, cleaned_data):
        phone = cleaned_data.get('phone')
        if phone and phone != int(User.objects.filter(user=self.request.user.id).first().phone):
            User.objects.filter(id=self.request.user.id).update(phone=phone)

    def validate_password(self, cleaned_data):
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if old_password:
            if authenticate(self.request, username=self.request.user.username, password=old_password):
                if self.check_password(new_password, confirm_new_password, self.request.user.username):
                    _user = user.objects.get(username=self.request.user.username)
                    _user.set_password(new_password.strip())
                    _user.save()
                else:
                    self.add_error('new_password', 'Invalid new password')
            else:
                self.add_error('old_password', 'Incorrect password')


class UploadImageForm(forms.Form):
    image = forms.ImageField()

    def __init__(self, prod, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prod = prod
        self.model = model

    def save(self):
        if self.model == "product":
            images = json.loads(self.prod.image)
            images['img/product-img'] += [self.upload().split('/')[-1]]
            images = str(images)
            self.prod.image = images.replace("'", '"')
        elif self.model in ["review", "fashion", "fashionmini", "hot"]:
            self.prod.image = 'img/product-img/' + self.upload().split('/')[-1]
        self.prod.save()

    def upload(self):
        img = self.cleaned_data["image"]
        obj = UploadImage(img=img)
        obj.save()
        return str(obj.img)
