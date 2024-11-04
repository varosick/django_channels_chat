from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from .models import Group
from django.contrib.auth.decorators import login_required


@login_required
def home_view(request):
    '''Home page that lists all the groups'''
    groups = Group.objects.all()
    user = request.user
    context = {
        "groups": groups,
        "user": user
    }
    return render(request, template_name="chat/home.html", context=context)


@login_required
def group_chat_view(request, uuid):
    '''A view for the group where all messages and events are sent to the interface'''

    group = get_object_or_404(Group, uuid=uuid)
    if request.user not in group.members.all():
        return HttpResponseForbidden("You are not a member of this group.\
                                       Kindly use the join button")

    messages = group.message_set.all()
    events = group.event_set.all()
    ''' Events are messages that indicate
    That a user has joined or left a group.
    They will be sent automatically when the user joins or leaves the group.
    '''

    # Sort by timestamp so that they are listed in order
    message_and_event_list = [*messages, *events]
    sorted_message_event_list = sorted(message_and_event_list, key=lambda x: x.timestamp)

    group_members = group.members.all()

    context = {
        "message_and_event_list": sorted_message_event_list,
        "group_members": group_members,
    }

    return render(request, template_name="chat/groupchat.html", context=context)
