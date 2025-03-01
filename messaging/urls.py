from django.urls import path
from .views import get_or_create_conversation, send_message, chatInterface

urlpatterns = [
    path("chat/<int:user_id>/", get_or_create_conversation, name="chat"),  # Finding or creating a conversation
    path("chat/conversation/<int:conversation_id>/", send_message, name="send_message"),  # Sending messages
    path("chat/", chatInterface, name="chatInterface")  # Chat interface
]
