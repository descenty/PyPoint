from rest_framework import serializers
from .models import Customer, PickPoint


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
    


class PickPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickPoint
        fields = ('address', 'owner')


class PickPointDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickPoint
        fields = '__all__'
