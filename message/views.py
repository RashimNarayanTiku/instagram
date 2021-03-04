from message.models import Inbox, Message
from post.owner import  OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from datetime import timedelta

from django.core import serializers
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
import pytz
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import MessageForm


@login_required
def InboxListView(request):
    ctx = {}
    if request.method == 'POST':
        pass
    else:
        inboxes = Inbox.objects.filter(owner=request.user)
        ctx = {'inboxes':inboxes}
    return render(request, 'message/inbox.html', ctx)


@login_required
def InboxDetailView(request, pk):

    if request.is_ajax():
        message_form = MessageForm()
        inbox = Inbox.objects.get(id=pk)

        owner = inbox.owner.id
        reciever = inbox.reciever.id

        owner_messages = inbox.owner_messages.all() 
        reciever_messages = inbox.reciever_messages.all() 

        messages = owner_messages | reciever_messages

        html = render_to_string('message/inbox_detail.html', {'inbox':inbox, 'messages':messages, 'owner_messages':owner_messages, 
                                                              'reciever_messages':reciever_messages, 'message_form':message_form})

        return JsonResponse(data={'html':html}, safe=False)
    
    return redirect('inbox_list')



@login_required
def MessageCreateView(request, pk):
    owner_inbox = Inbox.objects.get(id=pk)
    
    owner = User.objects.get(id=owner_inbox.owner.id)
    reciever = User.objects.get(id=owner_inbox.reciever.id)
    try:
        reciever_inbox = Inbox.objects.get(owner=reciever, reciever=owner)
    except Inbox.DoesNotExist:
        reciever_inbox = Inbox.objects.create(owner=reciever, reciever=owner)

    response_data = {}
    
    if request.POST.get('action') == 'post':
        text = request.POST.get('text')
        message = Message.objects.create(
            text = text,
            owner_inbox = owner_inbox,
            reciever_inbox = reciever_inbox,
        )

        format = "%B %d, %Y"
        time = message.created_at.strftime(format)
        response_data['text'] = text
        response_data['created_at'] = time
        response_data['inbox_id'] = pk
        
        return JsonResponse(response_data)    
    return redirect('inbox_list') 



@login_required
def MessageUpdateView(request, pk):

    if request.is_ajax():
        inbox = Inbox.objects.get(id=pk)

        owner = inbox.owner.id
        reciever = inbox.reciever.id

        time_threshold = timezone.now() - timedelta(seconds=4)

        # owner_messages = inbox.owner_messages.filter(created_at__gt=time_threshold) 
        reciever_messages = inbox.reciever_messages.filter(created_at__gt=time_threshold) 

        messages = reciever_messages

        html = render_to_string('message/messages.html', {'messages':messages})
        return JsonResponse(data={'html':html}, safe=False)
