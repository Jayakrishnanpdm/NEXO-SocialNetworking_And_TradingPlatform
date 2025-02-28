from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Conversation, Message
from django.contrib.auth.models import User

@login_required
def get_or_create_conversation(request, user_id):
    """ Get or create a chat between two users """
    user2 = get_object_or_404(User, id=user_id)
    
    # Ensure only ONE conversation exists between the two users
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=user2).first()
    
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, user2)

    messages = conversation.messages.all()
    return render(request, "networking/chat.html", {
        "conversation": conversation, 
        "messages": messages, 
        "conversation_id": conversation.id  # Pass conversation_id
    })

@login_required
def send_message(request, conversation_id):
    """ Send a new message """
    conversation = get_object_or_404(Conversation, id=conversation_id)
    content = request.POST.get("content")

    if content:
        message = Message.objects.create(conversation=conversation, sender=request.user, content=content)
        return JsonResponse({"message": message.content, "sender": message.sender.username, "timestamp": message.timestamp})

    return JsonResponse({"error": "Message cannot be empty"}, status=400)
