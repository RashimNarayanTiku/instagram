from django.db import models
from django.contrib.auth.models import User
from post.models import Post

class Inbox(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox_owner')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox_reciever')

    class Meta:
        unique_together = ('owner', 'reciever')

    def __str__(self) :
        return '%s -> %s' % (self.owner.username, self.reciever.username)


class Message(models.Model):

    text = models.CharField(max_length=250, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)

    owner_inbox = models.ForeignKey(Inbox, on_delete=models.CASCADE, default=None, related_name='owner_messages')
    reciever_inbox = models.ForeignKey(Inbox, on_delete=models.CASCADE, default=None, related_name='reciever_messages')
    created_at = models.DateTimeField(auto_now_add=True)

    sent = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']

    def __str__(self) :
        if self.post:
            if len(self.post.caption)>10:
                return '%s -> %s : [Post] %s...' % (self.owner_inbox.owner.username, self.reciever_inbox.owner.username, self.post.caption[:10])
            else:
                return '%s -> %s : [Post] %s' % (self.owner_inbox.owner.username, self.reciever_inbox.owner.username, self.post.caption)

        else:
            if len(self.text)>10:
                return '%s -> %s : [Message] %s...' % (self.owner_inbox.owner.username, self.reciever_inbox.owner.username, self.text[:10])
            else:
                return '%s -> %s : [Message] %s' % (self.owner_inbox.owner.username, self.reciever_inbox.owner.username, self.text)



