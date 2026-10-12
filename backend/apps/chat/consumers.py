import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        if not self.user.is_authenticated:
            await self.close()
            return


        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]

        is_participant = await Conversation.objects.filter(
            participants=self.user, id=self.conversation_id
        ).aexists()

        if not is_participant:
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

        message = data["message"]
        
        if len(message) > 1000:
            await self.send(json.dumps({"error": "Message too long"}))
            return
        
        if len(message) < 5:
            await self.send(json.dumps({"error": "Message too short"}))
            return

        if not isinstance(message, str):
            return

        msg = await Message.objects.acreate(
            conversation_id=self.conversation_id, sender=self.user, content=message
        )

        participant_ids = User.objects.filter(conversations__id=self.conversation_id).exclude(id=self.user.pk).values_list("pk", flat=True)
        async for participant in participant_ids:
            await self.channel_layer.group_send(
                f'user_{participant}',
                {
                    "type": "send.message",
                    "id": msg.id,
                    "conversation_id":msg.conversation_id,
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
                    "conversation_id":event["conversation_id"],
                    "message": event["message"],
                    "sender_id": event["sender_id"],
                    "created_at": event["created_at"],
                }
            )
        )

    async def disconnect(self, code_code):
        if hasattr(self, self.group_name):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
