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
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import MessageForm
from message.models import Inbox, Message
from notification.models import InboxNotification
from post.owner import  OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from datetime import timedelta
import pytz



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

        InboxNotification.objects.filter(inbox=inbox).delete()

        owner_messages = inbox.owner_messages.all() 
        reciever_messages = inbox.reciever_messages.all() 

        messages = owner_messages | reciever_messages

        html = render_to_string('message/inbox_detail.html', {'inbox':inbox, 'messages':messages, 'owner_messages':owner_messages, 
                                                              'reciever_messages':reciever_messages, 'message_form':message_form})

        return JsonResponse(data={'html':html}, safe=False)
    
    return redirect('inbox_list')




@method_decorator(csrf_exempt, name='dispatch')
@login_required
def InboxFindProfileView(request):
    if request.is_ajax():
        url_parameter = request.GET.get("q")
        if url_parameter:
            profiles = User.objects.filter(first_name__icontains=url_parameter)
        else:
            profiles = None

        html = render_to_string(
            template_name="message/new_inbox.html", 
            context={"profiles": profiles}
        )
        data_dict = {"html": html}
        return JsonResponse(data=data_dict, safe=False)



@method_decorator(csrf_exempt, name='dispatch')
@login_required
def InboxCreateView(request,pk):

    reciever = User.objects.get(id=pk)
    inbox = Inbox.objects.get_or_create(owner=request.user, reciever=reciever)
    return redirect(reverse("inbox_list"))




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

        notification = InboxNotification.objects.get_or_create(inbox=reciever_inbox)

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
        reciever = inbox.reciever

        time_threshold = timezone.now() - timedelta(seconds=3)
        reciever_messages = inbox.reciever_messages.filter(created_at__gt=time_threshold, sent=False)
        messages = reciever_messages

        for m in messages:
            m.sent = True
            m.save()

        html = render_to_string('message/messages.html', {'messages':messages, 'user':request.user, 'reciever':reciever})
        return JsonResponse(data={'html':html}, safe=False)
