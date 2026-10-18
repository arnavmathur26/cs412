from django import forms
from .models import Profile, Posts, Photo

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''A form to update an existing Profile.'''

    class Meta:
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']

class UpdatePostForm(forms.ModelForm):
    '''A form to update the caption of an existing Post.'''

    class Meta:
        model = Posts
        fields = ['caption']
