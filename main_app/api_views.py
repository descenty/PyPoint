from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from rest_framework.request import Request
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from main_app.in_memory_data import *
from .models import Vehicle
from .serializers import *
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, RetrieveAPIView
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
        return PickPoint.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        user_id = Token.objects.get(key=self.request.auth).user_id
        data = request.data
        data['owner'] = user_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(PickPointListSerializer(serializer.instance).data, status=status.HTTP_201_CREATED,
                        headers=headers)


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'create':
            return SellerCreateSerializer
        return SellerDetailSerializer


class GoodViewSet(viewsets.ModelViewSet):
    queryset = Good.objects.all()
    serializer_class = GoodSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CartGoodViewSet(viewsets.ModelViewSet):
    serializer_class = CartGoodSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return CartGood.objects.filter(cart__customer=self.request.user)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_cart(request):
    return Response(CartSerializer(Cart.objects.get(customer=request.user)).data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def post_vehicle_coords(request: Request):
    serializer = VehicleCoordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    get_object_or_404(Vehicle, id=data['vehicle_id'])
    vehicle_coords[data['vehicle_id']] = Coord(
        latitude=data['latitude'],
        longitude=data['longitude']
    )
    return HttpResponse(status=200)


class AddToCart(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        good_id = request.data['good_id']
        good = get_object_or_404(Good, id=good_id)
        cart: Cart = request.user.cart
        if cart.cart_goods.filter(good_id=good.id).exists():
            cart_good = cart.cart_goods.get(good_id=good.id)
            cart_good.quantity += 1
        else:
            cart_good = CartGood.objects.create(good_id=good.id, quantity=1, cart=request.user.cart)
        cart_good.save()
        return HttpResponse(status=200)
