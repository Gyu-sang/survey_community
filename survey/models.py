from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    link = models.URLField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField()
    finish = models.BooleanField(default=False)
    credit = models.PositiveIntegerField()
    max_participant = models.PositiveIntegerField()
    participant = models.PositiveIntegerField(blank=True)
    notice = models.BooleanField(default=False)



class Comment2(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    photo = models.ImageField()
    done = models.BooleanField(default=False)

    class Meta:
        unique_together = ('author', 'post')

class Withdraw(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    bank = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    credit = models.PositiveIntegerField()
    credit_wait = models.PositiveIntegerField()
    done = models.BooleanField()

class Deposit(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    bank = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    credit = models.PositiveIntegerField()
    credit_wait = models.PositiveIntegerField()
    done = models.BooleanField()
