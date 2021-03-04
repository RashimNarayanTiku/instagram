from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Profile


#using first_name as full_name 
class SignUpForm(UserCreationForm):
    username   = forms.CharField(widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})))
    first_name = forms.CharField(widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'})), max_length=32, help_text='Full name')
    email      = forms.EmailField(widget=(forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})), max_length=64, help_text='Enter a valid email address')
    password1  = forms.CharField(widget=(forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})))
    password2  = forms.CharField(widget=(forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'})))

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f"Another account is using {email}")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username isn't available. Please try another.")

        return self.cleaned_data

    class Meta:
        model = User
        fields = ('email', 'first_name','username', 'password1','password2')


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or email', 'id': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'password', 'id': 'password'}))


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo','website','bio', 'phone']
