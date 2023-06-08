from django.contrib import admin
from .models import Product, Promo, User, Review, Fashion, FashionMini, Hot, SocialMedia, Comment, Category, \
    EmailVerification

import json


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ['slug', 'image']
    list_display = ['name', 'type', 'subtype', 'color', 'price', 'image_tag']
    search_fields = ['name', 'type', 'subtype', 'color', 'price']
    list_filter = ['type', 'subtype', 'color']
    list_editable = ['price']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['mail', '__comment__']
    search_fields = ['mail', 'comment']
    list_filter = ['mail']


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ['promo', 'discount', 'count', 'access']
    list_filter = ['access']
    search_fields = ['promo', 'discount', 'count', 'access']
    list_editable = ['discount', 'count', 'access']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', '__review__', 'image_tag']
    search_fields = ['name', 'review']
    exclude = ['image']


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['social', 'data']
    search_fields = ['social', 'data']
    list_editable = ['data']
    readonly_fields = ['social']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']
    search_fields = ['user', 'phone']
    readonly_fields = ['user', 'user_login']


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'expiration']
    fields = ['code', 'user', 'expiration', 'created']
    readonly_fields = ['created']

@admin.register(Fashion)
class FashionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'button_text', 'image_tag']
    search_fields = ['name', 'description', 'button_text']
    list_editable = ['name', 'description', 'button_text']
    exclude = ['image']


@admin.register(FashionMini)
class FashionMiniAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'button_text', 'image_tag']
    search_fields = ['name', 'description', 'button_text']
    list_editable = ['name', 'description', 'button_text']
    exclude = ['image']


@admin.register(Hot)
class HotAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'prev_price', 'price', 'image_tag']
    search_fields = ['name', 'description', 'prev_price', 'price']
    list_editable = ['name', 'description', 'prev_price', 'price']
    exclude = ['image']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['type', 'subtype']
    search_fields = ['type', 'subtype']
    list_filter = ['type']
