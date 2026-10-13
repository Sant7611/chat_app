from rest_framework.viewsets import ModelViewSet
from apps.chat.serializers.message_serializer import MessageSerializer, MessageCreateSerializer
from apps.chat.models import Message, Conversation
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from apps.chat.services.message_services import create_message



class MessageView(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        user = self.request.user
        return Message.objects.filter(conversation_id=conversation_id, conversation__participants=user).select_related('conversation','sender')
        

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MessageCreateSerializer
        else:
            return MessageSerializer
        
    
    def perform_create(self, serializer):
        conversation_id = self.kwargs['conversation_id']
        serializer.save(conversation_id=conversation_id, sender=self.request.user)