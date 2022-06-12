from django.shortcuts import render
from .models import *


def index(request):
    return render(request, 'index.html')


def seller(request):
    return render(request, 'seller.html')


def register(request):
    return render(request, 'seller.html')


def login(request):
    return render(request, 'seller.html')

