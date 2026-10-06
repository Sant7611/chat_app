from django.urls import path, include
from apps.chat.views import conversation_view, message_view
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('',message_view.MessageView, basename='messages')

urlpatterns = [
    path('conversation/', conversation_view.ConversastionView.as_view(), name='conversation'),
    path('conversation/<int:conversation_id>/messages/', include(router.urls)),
]
