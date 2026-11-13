from django.db import models
from django.urls import reverse
from django.templatetags.static import static
from django.contrib.auth.models import User
# Create your models here.

class Joke(models.Model):
    joke = models.TextField(blank=False)
    contributor = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)


class Picture(models.Model):
    image_url = models.TextField(blank=False)
    contributor = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)