from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Conversation, Message
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Max

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
    group_chats = Conversation.objects.filter(is_groupchat=True, participants=request.user).order_by("-id")
    now = timezone.now() 
    context={
        'conversation':conversation,
        'messages':messages,
        'users':users,
        'group_chats':group_chats,
        'receiver':receiver,
        'now':now
    }
    return render(request, "networking/privateChat.html", context)

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
    group_chats = Conversation.objects.filter(is_groupchat=True, participants=request.user).order_by("-id")
    return render(request, "networking/chatInterface.html", {"users": users, "group_chats": group_chats})


@login_required
def group_chat(request, group_id):
    """ Fetch an existing group chat or create a new one """

    # Try to get the group conversation, or create one if it doesn't exist
    conversation, created = Conversation.objects.get_or_create(
        id=group_id,
        defaults={"is_groupchat": True}  # Ensure it is a group chat
    )
    group_name=conversation.groupname
    # If the conversation was just created, add the requesting user as a participant
    if created:
        conversation.participants.add(request.user)

    messages = conversation.messages.all().order_by("timestamp")  # Get messages
    users = User.objects.exclude(id=request.user.id)  # Get all users except current user
    group_chats = Conversation.objects.filter(is_groupchat=True, participants=request.user).order_by("-id")
    member_count = conversation.participants.count()
    members=conversation.participants.all().exclude(id=conversation.creator.id)
    context={
        'conversation':conversation,
        'messages':messages,
        'users':users,
        'group_name':group_name,
        'group_chats':group_chats,
        'member_count':member_count,
        'members':members,
        'group_creator': conversation.creator,
        'profile_pic':conversation.profile_pic
    }

    return render(request, "networking/groupchat.html", context)

def new_groupChat(request):
    if request.method == "POST":
        group_name = request.POST.get("group_name")
        group_pic = request.FILES.get("group_pic")
        members = request.POST.get("group_members")  # Comma-separated user list
        timespan_type = request.POST.get("timespan_type")
        timespan_value = request.POST.get("timespan_value")
        
        if not group_name:
            return render(request, "networking/groupChat.html", {"error": "Group name cannot be empty"})

        # Create the group chat
        conversation = Conversation.objects.create(
            is_groupchat=True,
            groupname=group_name,
            creator=request.user,
            timespan_type=timespan_type if timespan_type else "none",  # Default to "none" if not provided
            timespan_value=int(timespan_value) if timespan_value else 1,  # Ensure it's an integer
             
        )

        if group_pic:
            conversation.profile_pic = group_pic

        conversation.participants.add(request.user) 

        if members:
            member_list = [username.strip() for username in members.split(",")]  # Convert string to list
            for username in member_list:
                try:
                    user = User.objects.get(username=username)
                    conversation.participants.add(user)
                except User.DoesNotExist:
                    pass  # Ignore invalid users

        conversation.save()
        members=conversation.participants.all().exclude(id=conversation.creator.id)

        # Fetch all conversations for left-side chat list
        group_chats = Conversation.objects.filter(is_groupchat=True, participants=request.user).order_by("-id")
        context={
        'conversation':conversation,
        'users':User.objects.all().exclude(id=request.user.id),
        'group_name':group_name,
        'group_chats':group_chats,
        'member_count':conversation.participants.count(),
        'members' : members,
        'group_creator': conversation.creator,
        'profile_pic':conversation.profile_pic
    }

        return render(request, "networking/groupChat.html", context)

    return render(request, "networking/ChatInterface.html")

@login_required
def send_group_message(request, conversation_id):
    """ Send a message to the group chat """
    conversation = get_object_or_404(Conversation, id=conversation_id, is_groupchat=True)
    content = request.POST.get("content")

    if content:
        message = Message.objects.create(conversation=conversation, sender=request.user, content=content)
        return JsonResponse({"message": message.content, "sender": message.sender.username, "timestamp": message.timestamp})

    return JsonResponse({"error": "Message cannot be empty"}, status=400)

@login_required(login_url="/signup/")
def profile(request):
    user=request.user
    username=user.username
    return render(request, "networking/profile.html",{"username":username})

@login_required(login_url="/signup/")
def home(request):
    user=request.user
    username=user.username
    return render(request, "networking/home.html",{"username":username})