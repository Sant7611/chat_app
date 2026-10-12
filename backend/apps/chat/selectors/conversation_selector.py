from apps.chat.models import Conversation


def get_participant_ids(conversation_id, participants):
    return Conversation.objects.filter(id=conversation_id).values_list('participants__id', flat=True)