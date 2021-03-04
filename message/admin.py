from django.contrib import admin
from .models import Message, Inbox

admin.site.register(Message)
admin.site.register(Inbox)
