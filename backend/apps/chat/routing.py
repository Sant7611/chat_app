from .consumers import ChatConsumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/chat/<int:conversation_id>/', ChatConsumer.as_asgi(), name='chat_websocket')
]
