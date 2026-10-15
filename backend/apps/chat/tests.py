import pytest
from django.contrib.auth import get_user_model
from apps.chat.models import Conversation, Message
from apps.chat.services.message_services import create_message
from apps.chat.serializers.message_serializer import *

User= get_user_model()


@pytest.fixture
def chat_data(db):
    ram = User.objects.create_user(username='ram', password='ram123', email='ram@gmail.com')
    hari = User.objects.create_user(username='hari', password='hari123', email='hari@gmail.com')
    
    conversation = Conversation.objects.create()
    
    conversation.participants.add(ram, hari)
    
    return ram,hari,conversation


def test_create_message(chat_data):

    #Arrange
    ram, hari, conversation = chat_data
    
    #Act
    message = create_message(sender=ram, content='Hello hari how are you', conversation_id=conversation.pk)
    
    #Assert
    assert message.sender == ram
    assert message.content == 'Hello hari how are you'
    assert Message.objects.count() == 1
    assert message.conversation == conversation
    
    

def test_message_valid_serializer():
    serializer = MessageCreateSerializer(data={'content':'     Hello heyyy    '})
    
    assert serializer.is_valid() is True
    assert serializer.data['content'] == 'Hello heyyy'
    

@pytest.mark.parametrize(
    "content", ['', '  ', '\n\t']
)
def test_empty_message(content):
    serializer = MessageCreateSerializer(data={'content':content})
    
    assert serializer.is_valid() is False
    assert 'content' in serializer.errors