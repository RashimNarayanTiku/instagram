
# forms.py 
from django import forms 
from .models import *
  
# class PostForm(forms.ModelForm): 
#     class Meta: 
#         model = Post 
#         fields = ['name', 'hotel_Main_Img'] 

# strip removes whitespace from start and end before storing the column
class CommentForm(forms.Form):
    text = forms.CharField(required=False, max_length=250, min_length=1, strip=True, widget= forms.TextInput
                           (attrs={'placeholder':'Add a comment...'}))
