from django.contrib import admin
 
 
# Register your models here.
from .models import Profile, Photo, Posts, Follow, Comment, Like
admin.site.register(Profile)
admin.site.register(Photo)
admin.site.register(Posts)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)

 
 
