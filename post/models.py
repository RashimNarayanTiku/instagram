from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_posts')    
    photo = models.ImageField(upload_to="posts", default='default.jpg')
    caption = models.CharField(max_length=250,default='')

    created_at = models.DateTimeField(auto_now_add=True)
    
    comments = models.ManyToManyField(User, through='Comment', related_name='comment_post')
    likes = models.ManyToManyField(User, through='Like', related_name='like_post')
    saves = models.ManyToManyField(User, through='Save', related_name='save_post')

    def __str__(self):
        return f'{self.owner.username}: {self.caption[:15]}...'


class Like(models.Model) :
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('owner', 'post')

    def __str__(self) :
        return '%s likes %s... post'%(self.owner.username, self.post.caption[:15])


class Save(models.Model) :
    owner = models.ForeignKey(User, related_name='save_owner', on_delete=models.CASCADE)    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_saves')

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('owner', 'post')

    def __str__(self) :
        return '%s saved %s... post'%(self.owner.username, self.post.caption[:15])


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    text = models.CharField(max_length=250, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f'{self.owner.username}\'s comment on "{self.post.caption[:15]}..." post: {self.text}'

