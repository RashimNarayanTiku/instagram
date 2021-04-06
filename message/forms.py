
# forms.py 
from django import forms 
from .models import *
  

# strip removes whitespace from start and end before storing the column
class MessageForm(forms.Form):
    text = forms.CharField(required=False, max_length=250, min_length=1, widget= forms.TextInput(attrs={'placeholder':'Message...'}))
