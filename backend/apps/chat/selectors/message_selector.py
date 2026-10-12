from apps.chat.models import Message


def get_messages(*,conversation_id, participant):
    return Message.objects.filter(conversation=conversation_id, conversation__participants=participant).select_related('conversation', 'sender')