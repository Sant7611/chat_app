from .consumers import ChatConsumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/events/', ChatConsumer.as_asgi(), name='chat_websocket')
]
