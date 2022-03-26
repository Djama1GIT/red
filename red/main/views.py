from django.shortcuts import render
from django.views import View


class MainView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'red/index.html')


class CartView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'red/cart.html')


class ProdDetailsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'red/product-details.html')


class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'red/checkout.html')


class ShopView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'red/shop.html')