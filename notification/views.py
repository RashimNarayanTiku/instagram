from post.models import Post,Comment,Like,Save
from notification.models import InboxNotification, LikeNotification, CommentNotification

from django.core import serializers
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


class InboxNotificationView(View):

    def get(self, request):
        count = InboxNotification.objects.filter(inbox__owner=request.user).count()
        html = render_to_string(
            template_name="notification/inbox_notification.html", 
            context={"count": count}
        )
        response = {}
        response['html'] = html
        return JsonResponse(response)
        
        