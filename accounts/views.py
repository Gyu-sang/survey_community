from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.conf import settings
from .forms import SignupForm
# from .forms import LoginForm
# from django.contrib.auth.views import login as auth_login
# from allauth.socialaccount.models import SocialApp
# from allauth.socialaccount.templatetags.socialaccount import get_providers


# Create your views here.
@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("accounts:login")
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {
        'form':form,
    })


# def login(request):
#     providers = []
#     for provider in get_providers():
#         try :
#             provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)
#         except SocialApp.DoesNotExist:
#             provider.social_app = None
#         providers.append(provider)
#         return auth_login(request,
#             authentication_form = LoginForm,
#             template_name = 'accounts/login_form.html',
#             extra_context ={'providers':providers})










#
# signup = CreateView.as_view(model=User,
#     form_class=UserCreationForm,
#     success_url = settings.LOGIN_URL,
#     template_name = "accounts/signup.html")
