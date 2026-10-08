from django.db import models
from django.urls import reverse
from django.templatetags.static import static

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

    def get_posts(self):
        posts = Posts.objects.filter(profile=self)
        return posts

class Posts(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=False, default='')

    def __str__(self):
        return f'{self.profile.username}: {self.caption}'

    def get_absolute_url(self):
        '''Return the URL to display this Post.'''
        return reverse('show_post', kwargs={'pk': self.pk})

    def get_photos(self):
        photos = Photo.objects.filter(post=self)
        return photos


class Photo(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    image_url = models.TextField(blank=True, default='')
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def get_image_url(self):
        '''Return the URL to this Photo's image, whether stored as a URL or an uploaded file.'''
        if self.image_url:
            return static(self.image_url)
        return self.image_file.url

    def __str__(self):
        if self.image_url:
            return f'{self.post.profile.username}: {self.image_url} - {self.post.caption}'
        return f'{self.post.profile.username}: {self.image_file.name} - {self.post.caption}'
