from django.db import models
from django.contrib.auth.models import User


class Inbox(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox_owner')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox_reciever')

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('owner', 'reciever')

    def __str__(self) :
        return '%s -> %s' % (self.owner.username, self.reciever.username)


class Message(models.Model):

    text = models.CharField(max_length=250, null=False)
    owner_inbox = models.ForeignKey(Inbox, on_delete=models.CASCADE, default=None, related_name='owner_messages')
    reciever_inbox = models.ForeignKey(Inbox, on_delete=models.CASCADE, default=None, related_name='reciever_messages')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']

    def __str__(self) :
        return '%s -> %s :  %s' % (self.owner_inbox.owner.username, self.reciever_inbox.owner.username, self.text[:15])


# class Image(models.Model):
#   pass