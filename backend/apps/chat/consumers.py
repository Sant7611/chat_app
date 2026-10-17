import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversation, Message
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from apps.chat.services.message_services import create_message
from django.http import Http404

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        self.group_name = f"user_{self.user.pk}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

        await self.send(json.dumps({"success": "you connected successfully"}))

    async def receive(self, text_data=None, bytes_data=None):

        if text_data is None:
            return

        try:
            data = json.loads(text_data)

            if not isinstance(data, dict):
                return

        except json.JSONDecodeError:
            return
        message = data.get("message")
        conversation_id = data.get("conversation_id")

        if type(conversation_id) is not int or conversation_id <= 0:
            await self.send(
                text_data=json.dumps({"error": "Valid conversation_id required"})
            )

            return

        if not isinstance(message, str):
            await self.send(text_data=json.dumps({"error": "Message must be a string"}))
            return

        message = message.strip()

        if not message:
            await self.send(text_data=json.dumps({"error": "Message cannot be empty"}))
            return

        if len(message) > 1000:
            await self.send(text_data=json.dumps({"error": "Message too long"}))
            return

        try:
            msg = await database_sync_to_async(create_message)(
                conversation_id=conversation_id, sender=self.user, content=message
            )
        except Http404:

            await self.send(text_data=json.dumps({"error": "No conversation found"}))

            return

        participant_ids = (
            User.objects.filter(conversations__id=conversation_id)
            .exclude(id=self.user.pk)
            .values_list("pk", flat=True)
        )
        async for participant in participant_ids:
            await self.channel_layer.group_send(
                f"user_{participant}",
                {
                    "type": "send.message",
                    "id": msg.id,
                    "conversation_id": msg.conversation_id,
                    "message": msg.content,
                    "sender_id": str(msg.sender_id),
                    "created_at": msg.created_at.isoformat(),
                },
            )

    async def send_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "id": event["id"],
                    "conversation_id": event["conversation_id"],
                    "message": event["message"],
                    "sender_id": event["sender_id"],
                    "created_at": event["created_at"],
                }
            )
        )

    async def disconnect(self, code_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
