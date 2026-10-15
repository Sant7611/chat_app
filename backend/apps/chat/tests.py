import pytest
from django.contrib.auth import get_user_model
from apps.chat.models import Conversation, Message
from apps.chat.services.message_services import create_message
from apps.chat.serializers.message_serializer import *
from django.http import Http404
from rest_framework.test import APIClient
from django.urls import reverse

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
    assert serializer.validated_data['content'] == 'Hello heyyy'
    

@pytest.mark.parametrize(
    "content", ['', '  ', '\n\t']
)
def test_empty_message(content):
    serializer = MessageCreateSerializer(data={'content':content})
    
    assert serializer.is_valid() is False
    assert 'content' in serializer.errors
    
    

def test_unauthorized_user_cannot_send_message(chat_data):
    #Arrange
    ram, hari, conversation = chat_data
    
    outsider = User.objects.create_user(username='outsider', email='outsider@gmail.com', password='outsider123')
    
    #Act 
    with pytest.raises(Http404):
        create_message(conversation_id=conversation.id, content='Outsider message', sender=outsider)
        
    #Assert 
    assert Message.objects.count() == 0
    

def test_message_nonexistent_conversation(chat_data):
    #Arrange
    ram, hari, conversation = chat_data
    
    outsider = User.objects.create_user(username='outsider', email='outsider@gmail.com', password='outsider123')
    
    #Act 
    with pytest.raises(Http404):
        create_message(conversation_id=conversation.id+288, content='Outsider message', sender=outsider)
        
    #Assert 
    assert Message.objects.count() == 0
    

def test_participant_can_send_message_api(chat_data):
    #Arrange
    ram, hari, conversation = chat_data
    
    client = APIClient()
    client.force_authenticate(user=ram)
    
    url = reverse('messages', kwargs={'conversation_id':conversation.id})
    
    #Act
    response = client.post(url,{'content':'Hello hari this is ram'}, format='json')
    
    #Assert
    
    assert response.status_code == 201
    
    msg = Message.objects.get(conversation=conversation)
    
    
    assert msg.content == 'Hello hari this is ram'
    assert Message.objects.count() == 1