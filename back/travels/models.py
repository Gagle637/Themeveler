from django.db import models
from django.conf import settings
from django_mysql.models import ListTextField
from django.shortcuts import get_object_or_404

# Create your models here.
class Theme(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()
    region = models.CharField(max_length=50)
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True) # date is updated just created
    updated_at = models.DateTimeField(auto_now=True) # date is updated when created and updated
    visitors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='visited_themes', blank=True) # User.visited_themes.all()
    dests = ListTextField(
        base_field=models.CharField(max_length=255),
        size=100,
    )

    def __str__(self):
        return self.name

    def start(self):
        for num in self.dests:
            print(type(num))
            print(num)
            print()
        start_pk = int(self.dests[0])
        return get_object_or_404(Destination, pk=start_pk)
    

class Destination(models.Model):
    name = models.CharField(max_length=50)
    themes = models.ManyToManyField(Theme, related_name='spots', blank=True) # Theme.spots.all() / # Destination.themes.all -> return list
    image = models.ImageField(blank=True)
    latitude = models.CharField(max_length=100) # 위도
    longitude = models.CharField(max_length=100) # 경도
    created_at = models.DateTimeField(auto_now_add=True) # date is updated just created
    updated_at = models.DateTimeField(auto_now=True) # date is updated when created and updated
    visitors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dests', blank=True) # User.dests.all()
    
    def __str__(self):
        return self.name


class Message(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    nickname = models.CharField(blank=False, max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class DestContent(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE) # Content.objects.get(theme=theme_id, destination=destination_id)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    text = models.TextField()
