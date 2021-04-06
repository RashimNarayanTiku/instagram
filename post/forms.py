
# forms.py 
from django import forms 
from .models import *

class CommentForm(forms.Form):
    text = forms.CharField(required=False, max_length=250, min_length=1, strip=True, widget= forms.TextInput(attrs={'placeholder':'Add a comment...'}))


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('photo', 'caption') 
        widgets = {
            'photo': forms.FileInput(attrs={'id':'file-upload'}),
            'caption': forms.TextInput(attrs={'placeholder': 'Add a caption...', 'class':'post-create-form'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['caption'].label = ""
