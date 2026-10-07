from django.db import models
from django.urls import reverse

# Create your models here.


class Profile(models.Model):
    '''Encapsulate the idea of an Article by some author.'''

    # data attributes of a Article:
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.TextField(blank=False)
    bio_text = models.TextField(blank=False, default='')
    join_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        '''Return the URL to display this Profile.'''
        return reverse('show_profile', kwargs={'pk': self.pk})

class Posts(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=False)

    def __str__(self):
        return f'{self.profile.username}: {self.caption}'