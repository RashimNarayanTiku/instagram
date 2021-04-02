from post.models import Post,Comment,Like,Save
from user.models import Follow
from notification.models import InboxNotification, LikeNotification, CommentNotification, FollowNotification
from message.models import Inbox

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
from itertools import chain



class InboxNotificationView(View):

    def get(self, request, pk):

        if pk != 00:
            inbox = Inbox.objects.get(id=pk)
            InboxNotification.objects.filter(inbox=inbox).delete()
                    
        notifications = InboxNotification.objects.filter(inbox__owner=request.user)
        count = notifications.count()
        notifications = [ n.inbox.id for n in notifications ]
        

        html = render_to_string(
            template_name="notification/inbox_notification.html", 
            context={"count": count}
        )
        response = {}
        response['html'] = html
        response['notifications'] = notifications

        return JsonResponse(response)
        
        

class NotificationView(View):

    def get(self, request, pk):
        
        user = User.objects.get(id=pk)
        like_notifications = LikeNotification.objects.filter(like__post__owner=user)
        comment_notifications = CommentNotification.objects.filter(comment__post__owner=user)
        follow_notifications = FollowNotification.objects.filter(follow__reciever=user)

        html = render_to_string(
            template_name="notification/notification.html", 
            context={"like_notifications":like_notifications, 'comment_notifications':comment_notifications, 'follow_notifications':follow_notifications}
        )
        response = {}
        response['html'] = html
        response['count'] = like_notifications.count() + comment_notifications.count() + follow_notifications.count()
        return JsonResponse(response)
    

        
class NotificationDisplayView(View):

    def get(self, request, pk):
        
        user = User.objects.get(id=pk)

        try:
            LikeNotification.objects.filter(like__post__owner=user).delete()
            CommentNotification.objects.filter(comment__post__owner=user).delete()
            FollowNotification.objects.filter(follow__reciever=user).delete()

        except:
            pass
        
        likes = Like.objects.filter(post__owner=user)
        comments = Comment.objects.filter(post__owner=user)
        follows = Follow.objects.filter(reciever=user)
        
        notifications = sorted(
            chain(likes, comments, follows),
            key=lambda notification: notification.created_at, reverse=True)

        if len(notifications) <= 1:
            notifications = None

        html = render_to_string(
            template_name='notification/notification_display.html', 
            context = {'notifications':notifications, 'likes':likes, 'comments':comments, 'follows':follows, 'user':user}
        )
        response = {}
        response['html'] = html
        return JsonResponse(response)