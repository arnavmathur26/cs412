from django.db import models
from django.urls import reverse
from django.templatetags.static import static
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    '''Encapsulate the idea of an Article by some author.'''

    # data attributes of a Article:
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.TextField(blank=False)
    bio_text = models.TextField(blank=False, default='')
    join_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        '''Return the URL to display this Profile.'''
        return reverse('show_my_profile', kwargs={'pk': self.pk})

    def get_posts(self):
        posts = Posts.objects.filter(profile=self)
        return posts

    def get_followers(self):
        '''Return a list of the Profiles that follow this Profile.'''
        followers = []
        for follow in Follow.objects.filter(profile=self):
            followers.append(follow.follower_profile)
        return followers

    def get_num_followers(self):
        '''Return how many Profiles follow this Profile.'''
        return len(self.get_followers())

    def get_following(self):
        '''Return a list of the Profiles that this Profile follows.'''
        following = []
        for follow in Follow.objects.filter(follower_profile=self):
            following.append(follow.profile)
        return following

    def get_num_following(self):
        '''Return how many Profiles this Profile follows.'''
        return len(self.get_following())

    def get_post_feed(self):
        '''Return the Posts by the Profiles this Profile follows, newest first.'''
        posts = Posts.objects.filter(profile__in=self.get_following()).order_by('-timestamp')
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

    def get_all_comments(self):
        '''Return all Comments on this Post.'''
        comments = Comment.objects.filter(post=self)
        return comments

    def get_likes(self):
        '''Return all Likes on this Post.'''
        likes = Like.objects.filter(post=self)
        return likes


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


class Follow(models.Model):
    '''A Profile (follower_profile) following another Profile (profile).'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string showing who follows whom.'''
        return f'{self.follower_profile.display_name} follows {self.profile.display_name}'


class Comment(models.Model):
    '''A Comment made by a Profile on a Post.'''

    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=False)

    def __str__(self):
        '''Return a string showing the Comment and who wrote it.'''
        return f'{self.profile.username} on post {self.post.pk}: {self.text}'


class Like(models.Model):
    '''A Like from a Profile on a Post.'''

    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string showing who liked which Post.'''
        return f'{self.profile.username} likes post {self.post.pk}'
