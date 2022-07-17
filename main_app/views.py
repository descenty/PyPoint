from dataclasses import dataclass

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, CreateView
from django.shortcuts import render, redirect
from main_app.forms import CustomerCreationForm
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


class RegisterCustomerView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomerCreationForm

    def form_valid(self, form):
        customer = form.save()
        login(self.request, customer)
        return redirect('home')