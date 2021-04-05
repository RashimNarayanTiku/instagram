from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
import PIL.Image as Image

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profile_pics", default='default.jpg')
    website = models.URLField(default='', blank=True)
    bio = models.TextField(default='', blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+9999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)


    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.photo.path)
        width, height = img.size  # Get dimensions

        if width > 300 and height > 300:
            # keep ratio but shrink down
            img.thumbnail((width, height))

        # check which one is smaller
        if height < width:
            # make square by cutting off equal amounts left and right
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))

        elif width < height:
            # make square by cutting off bottom
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 300 and height > 300:
            img.thumbnail((300, 300))

        img.save(self.photo.path)


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
