from django.db import models
from django.utils.text import slugify


class User(models.Model):
    login = models.CharField('Login', max_length=16)
    password = models.TextField('Password')
    phone = models.CharField('Phone number', max_length=16)
    mail = models.EmailField('Email')
    cart = models.JSONField('Cart')
    purchases = models.JSONField('Purchases')

    def __str__(self):
        return self.login


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
        self.slug = slugify(self.name)
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
