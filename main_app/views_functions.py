from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse

from main_app.models import CartGood, Good, Cart


def update_cart_promo_code(request):
    cart: Cart = request.user.cart
    cart.promo_code = request.POST.get('promo_code')
    cart.save()
    return HttpResponseRedirect(request.POST.get('next'))

