import json

from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model


class User(models.Model):
    user_login = models.CharField('username', max_length=48)
    user = models.ForeignKey(get_user_model(), db_column="user_id", on_delete=models.CASCADE)
    phone = models.CharField('Phone number', max_length=16)
    cart = models.JSONField('Cart', null=True, default=json.dumps({}))

    def __str__(self):
        return self.user_login


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
    data = models.TextField('Data')

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
    name = models.TextField('The product\'s name')
    slug = models.SlugField(default='', null=False)
    gender = models.CharField('gender', max_length=8)
    type = models.TextField('type')
    subtype = models.TextField('subtype')
    sizes = models.TextField('sizes')
    price = models.FloatField('price')
    prev_price = models.FloatField('prev_price')
    color = models.CharField('color', max_length=6)
    image = models.TextField('image')

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.slug = slugify(self.name) + "-" + str(self.id)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Fashion(models.Model):
    name = models.TextField('name')
    description = models.TextField('description')
    button_text = models.TextField('button text')
    link = models.TextField('link')
    image = models.TextField('image')
    anim1 = models.CharField('anim1', max_length=16)
    anim2 = models.CharField('anim2', max_length=16)
    anim3 = models.CharField('anim3', max_length=16)
    prods = models.TextField('prods')

    def __str__(self):
        return self.name


class FashionMini(models.Model):
    name = models.TextField('name')
    description = models.TextField('description')
    button_text = models.TextField('button text')
    link = models.TextField('link')
    image = models.TextField('image')

    def __str__(self):
        return self.name


class Hot(models.Model):
    name = models.TextField('name')
    description = models.TextField('description')
    button_text = models.TextField('button text')
    link = models.TextField('link')
    image = models.TextField('image')
    prev_price = models.FloatField('prev price')
    price = models.FloatField('price')

    def __str__(self):
        return self.name


class Review(models.Model):
    name = models.CharField('name', max_length=64)
    review = models.TextField('review')
    image = models.TextField('image')
    address = models.TextField('The address')

    def __str__(self):
        return self.name


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
