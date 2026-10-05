from rest_framework.viewsets import ModelViewSet
from chat.serializers.message_serializer import MessageSerializer
from chat.models import Message


class MessageView(ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.select_related('conversation','sender')
    