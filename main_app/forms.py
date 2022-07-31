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

    def clean(self):
        cleaned_data = super(OrderCreationForm, self).clean()
        if cleaned_data.get('pick_point') is None and cleaned_data.get('delivery_point') is None:
            raise forms.ValidationError('Не указан пункт выдачи или адрес доставки')
        return cleaned_data

