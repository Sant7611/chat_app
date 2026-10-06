from rest_framework import serializers
from apps.chat.models import Message
from apps.chat.serializers.conversation_serializer import UserMiniSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserMiniSerializer(read_only=True)
    class Meta:
        model=Message
        fields =('id', 'content', 'sender', 'created_at')
        read_only_fields = fields
        

    

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('content',)

        
    def validate_content(self, value):
        value = value.strip()
        if value == '':
            raise serializers.ValidationError("Message cannot be empty")
        return value