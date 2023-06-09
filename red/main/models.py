from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.timezone import now

import json


class User(models.Model):
    user_login = models.CharField('username', max_length=48)
    user = models.ForeignKey(get_user_model(), db_column="user_id", on_delete=models.CASCADE)
    phone = models.CharField('Phone number', max_length=16)
    cart = models.JSONField('Cart', null=True, default=json.dumps({}))
    is_verified_email = models.BooleanField(default=False)

    def __str__(self):
        return self.user_login


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def send_verification_email(self):
        send_mail(
            "RED | Подтвердите адрес электронной почты",
            f"Здравствуйте, {self.user.username}!\n"
            f"Для подтверждения адреса вашей электронной почты({self.user.email}) перейдите по следующей ссылке:\n"
            f"{settings.DOMAIN}{reverse('email_verification', kwargs={'email': self.user.email, 'code': self.code})}\n"
            "Ссылка действительная в течение 24 часов.",
            "red@dj.ama1.ru",
            [self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False


class Purchase(models.Model):
    user_login = models.CharField('username', max_length=48)
    user = models.ForeignKey(get_user_model(), db_column="user_id", on_delete=models.CASCADE)
    first_name = models.CharField('first name', max_length=48)
    last_name = models.CharField('last name', max_length=48)
    country = models.CharField('country', max_length=48)
    address = models.CharField('address', max_length=48)
    postcode = models.CharField('postcode', max_length=48)
    city = models.CharField('city', max_length=48)
    province = models.CharField('province', max_length=48)
    product = models.CharField('product', max_length=128)
    slug = models.SlugField('slug', max_length=128)
    size = models.CharField('size', max_length=6)
    image = models.TextField('image')
    price = models.FloatField('price')
    datetime = models.DateTimeField('date', auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user_login) + ": " + str(self.product)


class SocialMedia(models.Model):
    social = models.CharField('Social', max_length=32)
    data = models.CharField('Data', max_length=48)

    def __str__(self):
        return self.social


class Promo(models.Model):
    promo = models.CharField('promo-code', max_length=16)
    description = models.TextField('Description')
    discount = models.IntegerField('Discount')
    count = models.IntegerField('Count of uses')
    access = models.CharField('access', max_length=16)
    color = models.CharField('color', max_length=6)  # if public and displayed on the main page

    def __str__(self):
        return self.promo


class Product(models.Model):
    genders = [
        ('unisex', 'Unisex'),
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    name = models.CharField('The product\'s name', max_length=96)
    slug = models.SlugField(default='', null=False)
    gender = models.CharField('gender', choices=genders, max_length=8)
    type = models.CharField('type', max_length=48)
    subtype = models.CharField('subtype', max_length=48)
    sizes = models.TextField('sizes', default=json.dumps({"XS": 15, "S": 15, "M": 15, "L": 15, "XL": 15, "XXL": 15}),
                             blank=True)
    price = models.FloatField('price')
    prev_price = models.FloatField('prev_price')
    rating = models.IntegerField('rating', default=0)
    color = models.CharField('color', max_length=6)
    image = models.TextField('image', default=json.dumps({"img/product-img": ["default.png"]}))

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        abc = Product.objects.latest('id').id + 1 if self.id is None else self.id
        self.slug = slugify(self.name) + "-" + str(abc)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def image_tag(self):
        for z, a in json.loads(self.image).items():
            self.image_url = z + "/" + a[0]
        return mark_safe(
            f'<a href="/admin/main/change-photo/product/{self.slug}"><img src='
            f'"{settings.STATIC_URL}{self.image_url}" style="max-height:50px" /></a>')  # Get Image url

    image_tag.short_description = 'Image(tap to change)'


class UploadImage(models.Model):
    img = models.ImageField(upload_to="red/main/static/img/product-img")


class Fashion(models.Model):
    name = models.CharField('name', max_length=32)
    description = models.CharField('description', max_length=64)
    button_text = models.CharField('button text', max_length=32)
    link = models.TextField('link')
    image = models.TextField('image')
    anim1 = models.CharField('anim1', max_length=16)
    anim2 = models.CharField('anim2', max_length=16)
    anim3 = models.CharField('anim3', max_length=16)
    prods = models.TextField('prods')

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe(
            f'<a href="/admin/main/change-photo/fashion/{self.id}"><img src='
            f'"{settings.STATIC_URL}{self.image}" style="max-height:50px" /></a>')  # Get Image url

    image_tag.short_description = 'Image(tap to change)'


class FashionMini(models.Model):
    name = models.CharField('name', max_length=32)
    description = models.CharField('description', max_length=64)
    button_text = models.CharField('button text', max_length=32)
    link = models.TextField('link')
    image = models.TextField('image')

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe(
            f'<a href="/admin/main/change-photo/fashionmini/{self.id}"><img src='
            f'"{settings.STATIC_URL}{self.image}" style="max-height:50px" /></a>')  # Get Image url

    image_tag.short_description = 'Image(tap to change)'


class Hot(models.Model):
    name = models.CharField('name', max_length=32)
    description = models.CharField('description', max_length=64)
    button_text = models.CharField('button text', max_length=32)
    link = models.TextField('link')
    image = models.TextField('image')
    prev_price = models.FloatField('prev price')
    price = models.FloatField('price')

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe(
            f'<a href="/admin/main/change-photo/hot/{self.id}"><img src='
            f'"{settings.STATIC_URL}{self.image}" style="max-height:50px" /></a>')  # Get Image url

    image_tag.short_description = 'Image(tap to change)'


class Review(models.Model):
    name = models.CharField('name', max_length=64)
    review = models.TextField('review')
    image = models.TextField('image')
    address = models.TextField('The address')

    def __str__(self):
        return self.name

    def __review__(self):
        return self.review[:96] + ("..." if len(self.review[:]) > 96 else "")

    def image_tag(self):
        return mark_safe(
            f'<a href="/admin/main/change-photo/review/{self.id}"><img src='
            f'"{settings.STATIC_URL}{self.image}" style="max-height:50px" /></a>')  # Get Image url

    image_tag.short_description = 'Image(tap to change)'


# Next time it's better to create 2 tables (type + subtype) and link them using FK
class Category(models.Model):
    type = models.CharField('type', max_length=48)
    subtype = models.CharField('subtype', max_length=48)

    def __str__(self):
        return self.type


class MailingList(models.Model):
    mail = models.CharField('mail', max_length=48)

    def __str__(self):
        return self.mail


class Comment(models.Model):
    name = models.TextField('name')
    lastname = models.TextField('lastname')
    mail = models.TextField('email')
    comment = models.TextField('comment')

    def __str__(self):
        return self.mail

    def __comment__(self):
        return self.comment[:64] + ("..." if len(self.comment[:]) > 64 else "")
