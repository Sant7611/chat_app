from django.db import models
from apps.core.models import BaseModel
from django.conf import settings


class Conversation(BaseModel):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="conversations"
    )
    
    def __str__(self):
        participants = ",".join([user.username for user in self.participants.all()])
        return participants


class Message(BaseModel):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.SET_NULL, null=True, related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages"
    )
    content = models.TextField()
    read_at = models.DateTimeField(null=True, blank=True)
