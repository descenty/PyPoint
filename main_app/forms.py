# accounts/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from django.forms import ModelForm

from .models import Customer, Order


class CustomerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("phone", 'fio',)
        field_classes = {"phone": UsernameField}


class OrderCreationForm(ModelForm):
    class Meta:
        model = Order
        fields = ('pick_point', 'delivery_point')
