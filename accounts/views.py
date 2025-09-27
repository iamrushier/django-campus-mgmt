from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import CMSUserCreationForm

class SignUpView(CreateView):
    form_class = CMSUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"