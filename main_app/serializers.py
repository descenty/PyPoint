from rest_framework import serializers
from .models import Customer, PickPoint, Good, Seller, CartGood


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
