from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from main_app.models import CartGood, Good, Cart


def update_cart_good(request, action):
    good = get_object_or_404(Good, id=request.POST.get('good_id'))
    cart: Cart = request.user.cart
    if cart.cart_goods.filter(good_id=good.id).exists():
        cart_good = cart.cart_goods.get(good_id=good.id)
        if action == 'add':
            cart_good.quantity += 1
            cart_good.save()
        elif action == 'delete':
            cart_good.quantity -= 1
            if cart_good.quantity == 0:
                cart_good.delete()
            else:
                cart_good.save()
    elif action == 'add':
        cart_good = CartGood.objects.create(good_id=good.id, quantity=1, cart=request.user.cart)
        cart_good.save()
    return HttpResponseRedirect(request.POST.get('next'))


def update_cart_promo_code(request):
    cart: Cart = request.user.cart
    cart.promo_code = request.POST.get('promo_code')
    cart.save()
    return HttpResponseRedirect(request.POST.get('next'))

