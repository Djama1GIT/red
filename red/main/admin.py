from django.contrib import admin
from .models import Product, Promo, User, Review, Fashion, FashionMini, Hot, Category

admin.site.register(User)
admin.site.register(Promo)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Fashion)
admin.site.register(FashionMini)
admin.site.register(Hot)
admin.site.register(Category)