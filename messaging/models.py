from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id} - {', '.join([user.username for user in self.participants.all()])}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)  # Single Tick
    seen = models.BooleanField(default=False) 

    class Meta:
        ordering = ["timestamp"]

    def mark_as_delivered(self):
        """Mark message as delivered when received by the WebSocket"""
        self.delivered = True
        self.save()

    def mark_as_seen(self):
        """Mark message as seen when the receiver opens the chat"""
        self.seen = True
        self.save()    

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"
