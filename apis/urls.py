# apis/urls.py
from django.urls import path
from .viewsets.accounts import SignupView, LoginView, LogoutView, CurrentUserView

app_name = "apis"

urlpatterns = [
    path("accounts/signup/", SignupView.as_view(), name="api_signup"),
    path("accounts/login/", LoginView.as_view(), name="api_login"),
    path("accounts/logout/", LogoutView.as_view(), name="api_logout"),
    path("accounts/user/", CurrentUserView.as_view(), name="api_user"),
]
