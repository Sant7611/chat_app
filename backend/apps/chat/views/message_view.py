from rest_framework.viewsets import ModelViewSet
from apps.chat.serializers.message_serializer import MessageSerializer, MessageCreateSerializer
from apps.chat.models import Message, Conversation
from django.shortcuts import get_object_or_404



class MessageView(ModelViewSet):
    serializer_class = MessageSerializer
    
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
        user = self.request.user
        
        conversation = get_object_or_404(Conversation, id=conversation_id,participants=user )
        
        serializer.save(conversation=conversation, sender=user)