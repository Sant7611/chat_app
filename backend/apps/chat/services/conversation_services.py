from apps.chat.models import Conversation


def get_or_create_conversation(user, other_user):

    conversation = (
        Conversation.objects.filter(participants=other_user.id)
        .filter(participants=user)
        .distinct()
        .first()
    )

    if conversation:
        return conversation

    conversation = Conversation.objects.create()

    conversation.participants.add(user, other_user)
    return conversation
