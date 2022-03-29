from django.db import models


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
    gender = models.IntegerField('gender')
    type = models.TextField('type')
    price = models.IntegerField('price')
    color = models.CharField('color', max_length=6)

    def __str__(self):
        return self.name
