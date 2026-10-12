from rest_framework.generics import ListCreateAPIView
from apps.chat.models import Conversation
from rest_framework.permissions import IsAuthenticated
from apps.chat.serializers.conversation_serializer import ConversationCreateSerializer, ConversastionSerializer


class ConversastionView(ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    
    
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).prefetch_related('participants').order_by('-updated_at')
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return ConversationCreateSerializer
        else:
            return ConversastionSerializer
