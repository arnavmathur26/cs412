from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Posts
from .forms import CreatePostForm

# Create your views here.

def main(request):
   '''Show the main page'''

   template_name = "main.html"
   return render(request, template_name)


class ProfileListView(ListView):
   '''Show all Profiles'''

   model = Profile
   template_name = "show_all_profiles.html"
   context_object_name = "profiles"


class ProfileDetailView(DetailView):
   '''Show a single Profile'''

   model = Profile
   template_name = "show_profile.html"
   context_object_name = "profile"

class CreatePostView(CreateView):
   form_class = CreatePostForm
   template_name = "create_post_form.html"


class PostDetailView(DetailView):
   '''Show a single Post'''

   model = Posts
   template_name = "show_post.html"
   context_object_name = "post"

