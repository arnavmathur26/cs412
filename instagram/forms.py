from django import forms
from .models import Profile, Posts, Photo

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['caption']

class CreateProfileForm(forms.ModelForm):
    '''A form to create a new Profile. The User is attached programmatically,
    not shown as a form field.'''

    class Meta:
        model = Profile
        fields = ['username', 'display_name', 'profile_image_url', 'bio_text']

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
