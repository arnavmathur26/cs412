from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Posts, Photo
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm

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



class UpdateProfileView(UpdateView):
   '''Handle updating an existing Profile.'''

   model = Profile
   form_class = UpdateProfileForm
   template_name = "update_profile_form.html"


class DeletePostView(DeleteView):
   '''Handle deleting a Post.'''

   model = Posts
   template_name = "delete_post_form.html"

   def get_context_data(self, **kwargs):
      '''Add the Post being deleted and its author's Profile to the context.'''

      context = super().get_context_data(**kwargs)
      context['post'] = self.object
      context['profile'] = self.object.profile
      return context

   def get_success_url(self):
      '''After deleting, go back to the author's Profile page.'''

      return reverse('show_profile', kwargs={'pk': self.object.profile.pk})


class UpdatePostView(UpdateView):
   '''Handle updating the caption of a Post.'''

   model = Posts
   form_class = UpdatePostForm
   template_name = "update_post_form.html"
   context_object_name = "post"


class ShowFollowersDetailView(DetailView):
   '''Show the followers of a Profile.'''

   model = Profile
   template_name = "show_followers.html"
   context_object_name = "profile"


class ShowFollowingDetailView(DetailView):
   '''Show the Profiles that a Profile follows.'''

   model = Profile
   template_name = "show_following.html"
   context_object_name = "profile"


class ShowFeedView(DetailView):
   '''Show the post feed for a Profile.'''

   model = Profile
   template_name = "show_feed.html"
   context_object_name = "profile"


class SearchView(ListView):
   '''Search for Profiles and Posts that match a query.'''

   template_name = "search_results.html"

   def dispatch(self, request, *args, **kwargs):
      '''Show the search form if there is no query, otherwise show the results.'''

      if 'query' not in self.request.GET:
         profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
         return render(request, "search.html", {'profile': profile})
      return super().dispatch(request, *args, **kwargs)

   def get_queryset(self):
      '''Return the Posts whose caption contains the query.'''

      query = self.request.GET['query']
      return Posts.objects.filter(caption__icontains=query)

   def get_context_data(self, **kwargs):
      '''Add the Profile, query, matching Posts, and matching Profiles to the context.'''

      context = super().get_context_data(**kwargs)
      query = self.request.GET['query']
      profiles = (Profile.objects.filter(username__icontains=query) |
                  Profile.objects.filter(display_name__icontains=query) |
                  Profile.objects.filter(bio_text__icontains=query))

      context['profile'] = get_object_or_404(Profile, pk=self.kwargs['pk'])
      context['query'] = query
      context['posts'] = self.get_queryset()
      context['profiles'] = profiles.distinct()
      return context
