from .models import SocialMedia, Category, User, Product
from django.core.cache import cache
from django.conf import settings

import json


def social_medias(request):
    return {
        'phone': cache.get_or_set('phone', SocialMedia.objects.filter(social='Phone number')[0].data, 15 * 60),
        'phone_ed': cache.get_or_set('phone_ed', SocialMedia.objects.filter(social='Phone number ed')[0].data, 15 * 60),
        'twitter': cache.get_or_set('twitter', SocialMedia.objects.filter(social='Twitter')[0].data, 15 * 60),
        'facebook': cache.get_or_set('facebook', SocialMedia.objects.filter(social='Facebook')[0].data, 15 * 60),
        'linkedIn': cache.get_or_set('linkedIn', SocialMedia.objects.filter(social='LinkedIn')[0].data, 15 * 60),
        'pinterest': cache.get_or_set('pinterest', SocialMedia.objects.filter(social='Pinterest')[0].data, 15 * 60)
    }


def categories(request):
    def get_categories():
        __categories = {}
        for i in Category.objects.order_by('id').iterator():
            if i.type in __categories:
                if i.subtype != "None":
                    __categories[i.type] += [i.subtype]
            else:
                __categories[i.type] = []
        return __categories

    _categories = cache.get_or_set('categories', get_categories(), 15 * 60)
    return {'categories': _categories}


def cart(request):
    if request.user.is_anonymous:
        return {}
    cat = User.objects.filter(user=request.user.id)[0].cart
    cat = json.loads(cat)
    _cart_ = {}
    cart_sum = 0
    for k, v in cat.items():
        product = Product.objects.filter(id=int(k))[0]
        sizes = dict(json.loads(product.sizes))
        count_sizes = 0
        if v in sizes.keys():
            count_sizes = sizes[v]
        for z, a in json.loads(product.image).items():
            product.image = z + "/" + a[0]
        if count_sizes > 0:
            cart_sum += product.price
        _cart_[product.name] = [product.price, product.image, product.slug, v, count_sizes, 1 if count_sizes > 1 else 0]
    cart_sum = float('{:.2f}'.format(cart_sum))
    return {'cart': [_cart_, cart_sum]}


def default(request):
    return {'STATIC_URL': settings.STATIC_URL,
            'sizes': ["XS", "S", "M", "L", "XL", "XXL"]}
