import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close()
            return

        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]

        is_participant = await Conversation.objects.filter(
            participants=self.user, id=self.conversation_id
        ).aexists()

        if not is_participant:
            await self.close()
            return

        self.group_name = f"chat_{self.conversation_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

        await self.send(json.dumps({"success": "you connected successfully"}))

    async def receive(self, text_data=None, bytes_data=None):

        if text_data is None:
            return

        try:
            data = json.loads(text_data)
            message = data["message"]
        except json.JSONDecodeError:
            return

        if not isinstance(data, dict):
            return

        if not isinstance(message, str):
            return

        msg = await Message.objects.acreate(
            conversation_id=self.conversation_id, sender=self.user, content=message
        )

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send.message",
                "id":msg.id,
                "message": msg.content,
                "sender_id": str(msg.sender_id),
                "created_at": msg.created_at.isoformat( ),
            },
        )

    async def send_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "id": event["id"],
                    "message": event["message"],
                    "sender_id": event["sender_id"],
                    "created_at": event["created_at"],
                }
            )
        )

    async def disconnect(self, code_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
