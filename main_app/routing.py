from django.urls import path
from main_app import consumers

websocket_urlpatterns = [
    path('', consumers.MessageRoomConsumer.as_asgi()),
]