from rest_framework.generics import ListCreateAPIView
from apps.chat.serializers.message_serializer import MessageSerializer, MessageCreateSerializer
from rest_framework.permissions import IsAuthenticated
from apps.chat.models import Message



class MessageView(ListCreateAPIView):
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