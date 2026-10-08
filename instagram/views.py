from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Posts, Photo
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
   '''Handle creating a new Post (and its Photos) for a given Profile.'''

   form_class = CreatePostForm
   template_name = "create_post_form.html"

   def get_context_data(self, **kwargs):
      '''Add the Profile (identified by the URL's pk) to the template context.'''

      context = super().get_context_data(**kwargs)
      profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
      context['profile'] = profile
      return context

   def form_valid(self, form):
      '''Attach the Profile to the new Post, save it, then create a Photo
      for each uploaded file.'''

      profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
      form.instance.profile = profile
      response = super().form_valid(form)

      files = self.request.FILES.getlist('files')
      for file in files:
         Photo.objects.create(post=self.object, image_file=file)

      return response


class PostDetailView(DetailView):
   '''Show a single Post'''

   model = Posts
   template_name = "show_post.html"
   context_object_name = "post"

