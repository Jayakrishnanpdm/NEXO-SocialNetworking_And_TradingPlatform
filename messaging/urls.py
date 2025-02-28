from django.urls import path
from .views import get_or_create_conversation, send_message

urlpatterns = [
    path("chat/<int:user_id>/", get_or_create_conversation, name="get_or_create_conversation"),  # Finding or creating a conversation
    path("chat/conversation/<int:conversation_id>/", send_message, name="send_message"),  # Sending messages
]
