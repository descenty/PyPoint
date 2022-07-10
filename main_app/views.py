from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from main_app.forms import CustomerCreationForm


class RegisterCustomerView(CreateView):
    template_name = 'registration/register.html'

    def get(self, request, **kwargs):
        context = {
            'form': CustomerCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            phone = form.cleaned_data.get('phone')
            password = form.cleaned_data.get('password')
            customer = authenticate(phone=phone, password=password)
            login(request, customer)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)