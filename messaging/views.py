from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Conversation, Message
from django.contrib.auth.models import User
from django.utils import timezone

@login_required(login_url="/signup/")
def get_or_create_conversation(request, user_id):
    """ Get or create a chat between two users """
    user2 = get_object_or_404(User, id=user_id)
    
    # Ensure only ONE conversation exists between the two users
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=user2).first()
    
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, user2)
    
    receiver = conversation.participants.exclude(id=request.user.id).first()

    messages = conversation.messages.all()
    users=User.objects.all().exclude(id=request.user.id)
    now = timezone.now() 
    return render(request, "networking/chat.html", {
        "conversation": conversation, 
        "messages": messages, 
        "conversation_id": conversation.id,
        "receiver": receiver ,
        "users": users,
        "now": now

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

def chatInterface(request):
    users=User.objects.all().exclude(id=request.user.id)
    return render(request, "networking/chatInterface.html", {"users": users})


@login_required
def group_chat(request, group_id):
    """ Fetch an existing group chat or create a new one """

    # Try to get the group conversation, or create one if it doesn't exist
    conversation, created = Conversation.objects.get_or_create(
        id=group_id,
        defaults={"is_groupchat": True}  # Ensure it is a group chat
    )

    # If the conversation was just created, add the requesting user as a participant
    if created:
        conversation.participants.add(request.user)

    messages = conversation.messages.all().order_by("timestamp")  # Get messages
    users = User.objects.exclude(id=request.user.id)  # Get all users except current user

    return render(request, "networking/sample_groupchat.html", {
        "conversation": conversation,
        "messages": messages,
        "users": users
    })

@login_required
def send_group_message(request, conversation_id):
    """ Send a message to the group chat """
    conversation = get_object_or_404(Conversation, id=conversation_id, is_group_chat=True)
    content = request.POST.get("content")

    if content:
        message = Message.objects.create(conversation=conversation, sender=request.user, content=content)
        return JsonResponse({"message": message.content, "sender": message.sender.username, "timestamp": message.timestamp})

    return JsonResponse({"error": "Message cannot be empty"}, status=400)