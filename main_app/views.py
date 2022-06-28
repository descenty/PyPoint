from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import *
from .serializers import *


# class CustomerViewSet(viewsets.ModelViewSet):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
#     permission_classes = (IsAuthenticated, )

class PickPointViewSet(viewsets.ModelViewSet):
    queryset = PickPoint.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        match self.action:
            case 'list' | 'create':
                return PickPointSerializer
        return PickPointDetailSerializer
