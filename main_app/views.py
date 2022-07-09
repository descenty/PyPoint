from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import *
from .serializers import *
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response


class CreateCustomerView(CreateAPIView):
    model = Customer
    serializer_class = CustomerSerializer
    permission_classes = [permissions.AllowAny]
     
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED, headers=headers)


class PickPointViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    
    def get_serializer_class(self):
        match self.action:
            case 'list':
                return PickPointListSerializer
            case 'create':
                return PickPointCreateSerializer
        return PickPointDetailSerializer

    def get_queryset(self):
        user_id = Token.objects.get(key=self.request.auth).user_id
        return PickPoint.objects.filter(owner_id=user_id)

    def create(self, request, *args, **kwargs):
        user_id = Token.objects.get(key=self.request.auth).user_id
        data = request.data
        data['owner'] = user_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(PickPointListSerializer(serializer.instance).data, status=status.HTTP_201_CREATED, headers=headers)


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.action == 'create':
            return SellerCreateSerializer
        return SellerDetailSerializer


class GoodViewSet(viewsets.ModelViewSet):
    queryset = Good.objects.all()
    serializer_class = GoodSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )