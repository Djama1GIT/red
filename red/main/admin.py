from django.contrib import admin
from .models import Product, Promo, User

admin.site.register(User)
admin.site.register(Promo)
admin.site.register(Product)