from django import forms
from .models import Profile

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'display_name', 'profile_image_url', 'bio_text']
