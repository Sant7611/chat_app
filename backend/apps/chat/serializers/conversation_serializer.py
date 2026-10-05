from rest_framework import serializers
from chat.models import Conversation
from django.contrib.auth import get_user_model

User = get_user_model()


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'display_name', 'email')

class ConversationCreateSerializer(serializers.ModelSerializer):
    other_user_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Conversation
        fields = ('id', 'other_user_id')
        
    def validate_other_user_id(self, value):
        request = self.context['request']
        
        if request.user.id == value:
            raise serializers.ValidationError("You cannot have conversation with yourself")

        if not Conversation.objects.get(id=value).exists():
            raise serializers.ValidationError("No User with that ID")
        
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        other_user_id = validated_data.pop['other_user_id']
        other_user = User.objects.get(id=other_user_id)
        
        conversation = Conversation.objects.create()
        
        conversation.participants.add(user, other_user)
        
        return conversation
    
    

class ConversastionSerializer(serializers.ModelSerializer):
    participants = UserMiniSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ('participants', 'id', 'created_at', 'updated_at')