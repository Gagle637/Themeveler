from django.db import models
from django.contrib.auth.models import AbstractUser
from travels.models import Theme, Destination
from articles.models import Comment, ReComment
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    username = models.EmailField(blank=False, max_length=254, unique=True)
    nickname = models.CharField(blank=False, max_length=20, unique=True)
    anonymous = models.CharField(blank=False, max_length=20, unique=True)
    banning_period = models.DateField(blank=True, null=True)
    favorite_themes = models.ManyToManyField(Theme, blank=True, related_name='theme_like_users') # Theme.theme_like_users.all()
    favorite_destinations = models.ManyToManyField(Destination, blank=True, related_name='destination_like_users') # Destination.destination_like_users.all()
    REQUIRED_FIELDS = ('nickname', 'anonymous',)


class Waiting(models.Model):
    username = models.EmailField(blank=False, max_length=254)
    is_confirm = models.BooleanField(default=False, blank=False)
    confirm_code = models.CharField(max_length=50, null=True)
    updated_at = models.DateTimeField(auto_now=True)