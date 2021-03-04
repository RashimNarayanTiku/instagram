from django.contrib import admin
from .models import Post,Like,Save,Comment

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Save)
admin.site.register(Comment)
