from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class Conversation(models.Model):
    TIMESLOT_CHOICES = [
        ("none", "No Expiry"),
        ("hours", "Hours"),
        ("days", "Days"),
        ("months", "Months"),
    ]

    participants = models.ManyToManyField(User, related_name="conversations")
    is_groupchat = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    groupname = models.CharField(max_length=100, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_groups")
    timespan_type = models.CharField(max_length=10, choices=TIMESLOT_CHOICES, default="none")
    timespan_value = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Calculate expiry time before saving"""
        if not self.pk:  # If new object, set expiry_at
            now = timezone.now()
            if self.timespan_type == "hours":
                self.expiry_at = now + timedelta(hours=self.timespan_value)
            elif self.timespan_type == "days":
                self.expiry_at = now + timedelta(days=self.timespan_value)
            elif self.timespan_type == "months":
                self.expiry_at = now + timedelta(days=self.timespan_value * 30)  # Approximate
            else:
                self.expiry_at = None  # No expiry for "none" option

        super().save(*args, **kwargs)

    def has_expired(self):
        """Check if the group has expired"""
        return self.expiry_at is not None and timezone.now() >= self.expiry_at

    def __str__(self):
        return f"Group: {self.groupname} (Expires: {self.expiry_at if self.expiry_at else 'Never'})"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages", null=True, blank=True)  # Only for private chats
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)  # Single Tick
    seen = models.BooleanField(default=False) 

    class Meta:
        ordering = ["timestamp"]

    def save(self, *args, **kwargs):
        """Ensure the receiver field is only set for private chats"""
        if self.conversation.is_groupchat:
            self.receiver = None  # No single receiver for group chats
        super().save(*args, **kwargs)

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
