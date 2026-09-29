from django.db import models

# Create your models here.
 
 
class Profile(models.Model):
    '''Encapsulate the idea of an Article by some author.'''
 
 
    # data attributes of a Article:
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.TextField(blank=False)
    bio_text = models.TextField(blank=False, default='')
    join_date = models.DateTimeField(auto_now=True)
    
 