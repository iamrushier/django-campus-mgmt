from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CMSUser

class CMSUserCreationForm(UserCreationForm):
    class Meta:
        model = CMSUser
        fields = ("username", "email", "password1", "password2")
