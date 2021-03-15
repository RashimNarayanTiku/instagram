from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from post.models import Post, Like, Comment
from user.models import Follow

from message.models import Inbox


class InboxNotification(models.Model):
    inbox = models.OneToOneField(Inbox, on_delete=models.CASCADE)

class LikeNotification(models.Model):
    like = models.OneToOneField(Like, on_delete=models.CASCADE)

class CommentNotification(models.Model):
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE)

class FollowNotification(models.Model):
    follow = models.OneToOneField(Follow, on_delete=models.CASCADE)

