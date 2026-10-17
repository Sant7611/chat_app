
import pytest

from channels.testing import WebsocketCommunicator
from config.asgi import application
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

from apps.chat.models import Conversation, Message

User = get_user_model()


@pytest.fixture
def ws_data(transactional_db, settings):
    settings.CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }

    ram = User.objects.create_user(
        username="ram",
        email="ram@gmail.com",
        password="password123"
    )

    hari = User.objects.create_user(
        username="hari",
        email="hari@gmail.com",
        password="password123"
    )

    sita = User.objects.create_user(
        username="sita",
        email="sita@gmail.com",
        password="password123"
    )

    conversation = Conversation.objects.create()
    conversation.participants.add(ram, hari)

    return ram, hari, sita, conversation


@pytest.mark.asyncio
async def test_websocket_connection_for_unauthenticated_user():
    communicator = WebsocketCommunicator( application , '/ws/events/' )
    
    connected, _= await communicator.connect()
    
    assert connected is False


@pytest.mark.asyncio
async def test_websocket_connection_for_authenticated_user(ws_data):
    ram, hari, sita, conversation = ws_data
    
    access_token = AccessToken.for_user(ram)
    
    communicator = WebsocketCommunicator( application , f'/ws/events/?token={access_token}' )
    
    connected, _= await communicator.connect()
    
    assert connected is True
    
@pytest.mark.asyncio
async def test_one_user_sends_msg_to_other_user(ws_data):
    ram, hari, sita, conversation = ws_data
    
    ram_access = AccessToken.for_user(ram)
    hari_access = AccessToken.for_user(hari)
    
    
    
    ram_ws = WebsocketCommunicator( application , f'/ws/events/?token={ram_access}' )
    hari_ws = WebsocketCommunicator( application , f'/ws/events/?token={hari_access}' )
    
    ram_connected, _= await ram_ws.connect()
    hari_connected, _= await hari_ws.connect()
    
    await ram_ws.receive_json_from()
    await hari_ws.receive_json_from()
    
    await ram_ws.send_json_to({
        'conversation_id':conversation.id,
        'message':'Hello hari'
    })
    
    event = await hari_ws.receive_json_from(timeout=3)
    
    assert event['sender_id'] == str(ram.id)
    assert event['message'] == 'Hello hari'