from rest_framework import serializers
from .models import Customer, PickPoint


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class PickPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickPoint
        fields = ('address', 'owner')


class PickPointDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickPoint
        fields = '__all__'
