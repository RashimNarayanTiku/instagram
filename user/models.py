from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profile_pics", default='default.jpg')
    website = models.URLField(default='', blank=True)
    bio = models.TextField(default='', blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+9999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    def __str__(self):
        return f'{self.user.username}'



class Follow(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')    
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('owner', 'reciever')

        
    def __str__(self):
        return f'{self.owner.username} follows {self.reciever.username}'




@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        Follow.objects.create(owner=instance, reciever=instance)
        rashim_narayan = User.objects.get(username='rashim_narayan')
        Follow.objects.create(owner=instance, reciever=rashim_narayan)



@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.user.save()
    pass
