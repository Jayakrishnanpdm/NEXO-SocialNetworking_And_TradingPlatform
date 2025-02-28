import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Conversation, Message
from channels.db import database_sync_to_async  

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """ Connect user to a WebSocket chat room using conversation ID """
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]

        # Validate conversation ID
        self.conversation = await self.get_conversation(self.conversation_id)
        if not self.conversation or not await self.is_user_in_conversation(self.user.id, self.conversation_id):
            await self.close()
            return

        # Room name is now the conversation ID
        self.room_group_name = f"chat_{self.conversation_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """ Disconnect user from WebSocket """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """ Receives a message and sends it to the chat group """
        data = json.loads(text_data)
        message = data.get("message", "").strip()

        if not message:
            return  # Ignore empty messages

        # Save message in the database
        saved_message = await self.save_message(self.conversation_id, self.user.id, message)

        # Broadcast the message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": saved_message.content,
                "sender_id": saved_message.sender.id,
                "sender_name": saved_message.sender.username,
                "timestamp": saved_message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    async def chat_message(self, event):
        """ Sends message to WebSocket """
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_conversation(self, conversation_id):
        """ Get conversation by ID """
        try:
            return Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return None

    @database_sync_to_async
    def is_user_in_conversation(self, user_id, conversation_id):
        """ Check if user is a participant in the conversation """
        return Conversation.objects.filter(id=conversation_id, participants__id=user_id).exists()

    @database_sync_to_async
    def save_message(self, conversation_id, sender_id, content):
        """ Save message to the database """
        sender = User.objects.get(id=sender_id)  # Retrieve sender safely
        conversation = Conversation.objects.get(id=conversation_id)  # Retrieve conversation safely
        return Message.objects.create(conversation=conversation, sender=sender, content=content)
