from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse
from rest_framework.test import APITestCase

from main_app.models import Customer, PickPoint
from main_app.serializers import PickPointSerializer
from rest_framework.authtoken.models import Token


class PickPointApiTestCase(APITestCase):
    def setUp(self):
        user1 = Customer.objects.create_user(phone='79200913521', password='12345678')
        user1.save()
        self.token1= Token.objects.create(user=user1)

        self.pickpoint1 = PickPoint.objects.create(address='г. Москва, Мукомольный проезд 2', owner=user1)
        self.pickpoint2 = PickPoint.objects.create(address='г. Москва, Мукомольный проезд 2с1', owner=user1)

    def test_get(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get('pick-points-list')
        serializer_data = PickPointSerializer([self.pickpoint1, self.pickpoint2], many=True).data
        print(serializer_data, response.data, sep='\n')
        self.assertEqual(serializer_data, response.data)
