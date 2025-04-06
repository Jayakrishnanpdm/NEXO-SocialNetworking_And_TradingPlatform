# tasks.py
from celery import shared_task
from django.utils import timezone

@shared_task
def disband_expired_group(conversation_id):
    """Disband a group chat if it has expired."""
    from .models import Conversation  # Import the Conversation model here to avoid circular imports
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        if conversation.has_expired():
            conversation.participants.clear()  # Remove all members
            conversation.creator = None  # Optionally set the creator to None
            conversation.save()
            # Optionally delete it too:
            conversation.delete()
    except Conversation.DoesNotExist:
        pass
