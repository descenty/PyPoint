from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse

from main_app.forms import OrderCreationForm
from main_app.models import *


def update_cart_promo_code(request: HttpRequest):
    cart: Cart = request.user.cart
    cart.promo_code = request.POST.get('promo_code')
    cart.save()
    return HttpResponseRedirect(request.headers.get('referer'))

