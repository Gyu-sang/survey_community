from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    credit = models.PositiveIntegerField(blank=True, default=1000)
    answer = models.PositiveIntegerField(blank=True, default=0)
    question = models.PositiveIntegerField(blank=True, default=0)

def on_post_save_for_user(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        Profile.objects.create(user=user)

post_save.connect(on_post_save_for_user, sender=settings.AUTH_USER_MODEL)
