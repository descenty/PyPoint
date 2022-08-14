from rest_framework import serializers
from .models import Customer, PickPoint, Good, Seller, CartGood, Cart, MessageRoom


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('phone', 'password')

    def create(self, validated_data):
        customer = Customer.objects.create_user(
            phone=validated_data['phone'],
            password=validated_data['password'],
        )
        return customer
    

class PickPointCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickPoint
        fields = ('address', 'owner')


class PickPointListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickPoint
        fields = ('address', 'rating')


class PickPointDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickPoint
        fields = '__all__'


class SellerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ('name', 'description')


class SellerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'


class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = '__all__'


class CartGoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartGood
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class VehicleCoordSerializer(serializers.Serializer):
    vehicle_id = serializers.IntegerField()
    latitude = serializers.DecimalField(max_digits=10, decimal_places=7)
    longitude = serializers.DecimalField(max_digits=10, decimal_places=7)


class MessageRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageRoom
        fields = '__all__'
        depth = 1
