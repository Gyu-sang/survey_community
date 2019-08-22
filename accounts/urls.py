from django.urls import path
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from . import views
from .forms import LoginForm

app_name = 'accounts'


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name="login"),
    # path('login/', auth_views.LoginView, {'authentication_form':LoginForm}, name="login"),
    # path('login/', views.login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('profile/', views.profile, name="profile"),
    path('signup/', views.signup, name="signup"),
]
