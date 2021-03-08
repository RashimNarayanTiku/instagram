from django.contrib import admin
from .models import InboxNotification, LikeNotification, CommentNotification

admin.site.register(InboxNotification)
admin.site.register(LikeNotification)
admin.site.register(CommentNotification)
