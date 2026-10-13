from django.core.exceptions import PermissionDenied
from apps.chat.models import Message, Conversation
from django.shortcuts import get_object_or_404


def create_message(*, conversation_id, content, sender):
    conversation = get_object_or_404(Conversation, participants=sender, id=conversation_id)
    
    message = Message.objects.create(sender=sender, content=content, conversation=conversation)
    return message