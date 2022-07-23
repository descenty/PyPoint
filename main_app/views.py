from dataclasses import dataclass

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.authtoken.models import Token

from main_app.forms import CustomerCreationForm, OrderCreationForm
from main_app.models import *
from main_app.utils import DataMixin


class HomeView(DataMixin, ListView):
    model = Good
    template_name = 'home.html'
    context_object_name = 'goods'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Домашняя страница')
        return context | c_def


class SellersView(DataMixin, ListView):
    model = Seller
    template_name = 'sellers.html'
    context_object_name = 'sellers'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Продавцы')
        return context | c_def


class CartView(DataMixin, DetailView):
    model = Cart
    template_name = 'cart.html'
    context_object_name = 'cart'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart: Cart = self.get_object()
        c_def = self.get_user_context(title='Корзина', total_difference=cart.total - cart.total_with_discount, user_token=Token.objects.get(user_id=self.request.user.id).key)
        if self.request.method == 'POST':
            c_def['form'] = OrderCreationForm(self.request.POST)
        else:
            c_def['form'] = OrderCreationForm()
        print(c_def)
        return context | c_def

    def get_object(self, **kwargs):
        return self.request.user.cart


class RegisterCustomerView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomerCreationForm

    def form_valid(self, form):
        customer = form.save()
        login(self.request, customer)
        return redirect('home')
