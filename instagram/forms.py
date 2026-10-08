from django import forms
from .models import Profile, Posts, Photo

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['caption']
