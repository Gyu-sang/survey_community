from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class SignupForm(UserCreationForm):
    class Meta:
        model=User
        widgets = {'password':forms.PasswordInput}
        fields = ['username','last_name','first_name','email']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
