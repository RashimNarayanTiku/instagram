from django.contrib import admin
from .models import Post,Like,Save,Comment,Reply

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Save)
admin.site.register(Comment)
admin.site.register(Reply)

