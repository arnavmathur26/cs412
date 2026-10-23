from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from .models import Profile, Posts, Photo, Follow, Like
from .forms import CreatePostForm, CreateProfileForm, UpdateProfileForm, UpdatePostForm

# Create your views here.

def main(request):
   '''Show the main page'''

   template_name = "main.html"
   return render(request, template_name)


class ProfileRequiredMixin(LoginRequiredMixin):
   '''LoginRequiredMixin plus a helper to find the Profile for the logged-in User.'''

   def get_login_url(self):
      '''Point LoginRequiredMixin at this app's own login view.'''

      return reverse('login')

   def get_profile(self):
      '''Return the Profile associated with the logged-in User.'''

      return Profile.objects.filter(user=self.request.user).first()


class CreateProfileView(CreateView):
   '''Show a combined User-registration + Profile-creation form, and create both.'''

   form_class = CreateProfileForm
   template_name = "create_profile_form.html"

   def get_context_data(self, **kwargs):
      '''Add an (unbound) UserCreationForm to the template context.'''

      context = super().get_context_data(**kwargs)
      context['user_creation_form'] = UserCreationForm()
      return context

   def form_valid(self, form):
      '''Create the User from the posted UserCreationForm data, log them in,
      then attach the new User to the Profile and delegate to the superclass.'''

      user_creation_form = UserCreationForm(self.request.POST)
      if not user_creation_form.is_valid():
         context = self.get_context_data()
         context['user_creation_form'] = user_creation_form
         return self.render_to_response(context)

      user = user_creation_form.save()
      login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
      form.instance.user = user
      return super().form_valid(form)


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

   def get_context_data(self, **kwargs):
      '''Flag whether the logged-in User owns this Profile, and whether they
      already follow it, for template decisions.'''

      context = super().get_context_data(**kwargs)
      is_owner = (self.request.user.is_authenticated and
                  self.object.user == self.request.user)
      context['is_owner'] = is_owner

      if self.request.user.is_authenticated and not is_owner:
         viewer_profile = Profile.objects.filter(user=self.request.user).first()
         context['is_following'] = Follow.objects.filter(
            profile=self.object, follower_profile=viewer_profile).exists()

      return context


class ShowMyProfileView(ProfileRequiredMixin, DetailView):
   '''Show the logged-in User's own Profile page.'''

   model = Profile
   template_name = "show_profile.html"
   context_object_name = "profile"

   def get_object(self, queryset=None):
      return self.get_profile()

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['is_owner'] = True
      return context


class CreatePostView(ProfileRequiredMixin, CreateView):
   '''Handle creating a new Post (and its Photos) for the logged-in User's Profile.'''

   form_class = CreatePostForm
   template_name = "create_post_form.html"

   def get_context_data(self, **kwargs):
      '''Add the logged-in User's Profile to the template context.'''

      context = super().get_context_data(**kwargs)
      context['profile'] = self.get_profile()
      return context

   def form_valid(self, form):
      '''Attach the Profile to the new Post, save it, then create a Photo
      for each uploaded file.'''

      profile = self.get_profile()
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

   def get_context_data(self, **kwargs):
      '''Flag whether the logged-in User owns this Post, and whether they
      already liked it, for template decisions.'''

      context = super().get_context_data(**kwargs)
      is_owner = (self.request.user.is_authenticated and
                  self.object.profile.user == self.request.user)
      context['is_owner'] = is_owner

      if self.request.user.is_authenticated and not is_owner:
         viewer_profile = Profile.objects.filter(user=self.request.user).first()
         context['is_liked'] = Like.objects.filter(
            post=self.object, profile=viewer_profile).exists()

      return context


class UpdateProfileView(ProfileRequiredMixin, UpdateView):
   '''Handle updating the logged-in User's own Profile.'''

   form_class = UpdateProfileForm
   template_name = "update_profile_form.html"

   def get_object(self, queryset=None):
      return self.get_profile()


class DeletePostView(ProfileRequiredMixin, DeleteView):
   '''Handle deleting a Post, if it belongs to the logged-in User.'''

   model = Posts
   template_name = "delete_post_form.html"

   def get_object(self, queryset=None):
      post = super().get_object(queryset)
      if post.profile.user != self.request.user:
         raise PermissionDenied("You can't delete another user's post.")
      return post

   def get_context_data(self, **kwargs):
      '''Add the Post being deleted and its author's Profile to the context.'''

      context = super().get_context_data(**kwargs)
      context['post'] = self.object
      context['profile'] = self.object.profile
      return context

   def get_success_url(self):
      '''After deleting, go back to the author's Profile page.'''

      return reverse('show_my_profile', kwargs={'pk': self.object.profile.pk})


class UpdatePostView(ProfileRequiredMixin, UpdateView):
   '''Handle updating the caption of a Post, if it belongs to the logged-in User.'''

   model = Posts
   form_class = UpdatePostForm
   template_name = "update_post_form.html"
   context_object_name = "post"

   def get_object(self, queryset=None):
      post = super().get_object(queryset)
      if post.profile.user != self.request.user:
         raise PermissionDenied("You can't update another user's post.")
      return post


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


class ShowFeedView(ProfileRequiredMixin, DetailView):
   '''Show the post feed for the logged-in User's own Profile.'''

   model = Profile
   template_name = "show_feed.html"
   context_object_name = "profile"

   def get_object(self, queryset=None):
      return self.get_profile()


class SearchView(ProfileRequiredMixin, ListView):
   '''Search for Profiles and Posts that match a query.'''

   template_name = "search_results.html"

   def get(self, request, *args, **kwargs):
      '''Show the search form if there is no query, otherwise show the results.'''

      if 'query' not in request.GET:
         return render(request, "search.html", {'profile': self.get_profile()})
      return super().get(request, *args, **kwargs)

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

      context['profile'] = self.get_profile()
      context['query'] = query
      context['posts'] = self.get_queryset()
      context['profiles'] = profiles.distinct()
      return context


class LogoutConfirmationView(TemplateView):
   '''Show a styled confirmation page after the User logs out.'''

   template_name = "logout.html"


class FollowProfileView(ProfileRequiredMixin, TemplateView):
   '''Create a Follow: the logged-in User's Profile follows another Profile.'''

   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()

      profile = self.get_profile()
      other_profile = get_object_or_404(Profile, pk=kwargs['pk'])
      if profile != other_profile:
         Follow.objects.get_or_create(profile=other_profile, follower_profile=profile)
      return redirect('show_my_profile', pk=other_profile.pk)


class DeleteFollowProfileView(ProfileRequiredMixin, TemplateView):
   '''Delete a Follow: the logged-in User's Profile unfollows another Profile.'''

   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()

      profile = self.get_profile()
      other_profile = get_object_or_404(Profile, pk=kwargs['pk'])
      Follow.objects.filter(profile=other_profile, follower_profile=profile).delete()
      return redirect('show_my_profile', pk=other_profile.pk)


class LikePostView(ProfileRequiredMixin, TemplateView):
   '''Create a Like: the logged-in User's Profile likes a Post.'''

   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()

      profile = self.get_profile()
      post = get_object_or_404(Posts, pk=kwargs['pk'])
      if post.profile != profile:
         Like.objects.get_or_create(post=post, profile=profile)
      return redirect('show_post', pk=post.pk)


class DeleteLikePostView(ProfileRequiredMixin, TemplateView):
   '''Delete a Like: the logged-in User's Profile un-likes a Post.'''

   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()

      profile = self.get_profile()
      post = get_object_or_404(Posts, pk=kwargs['pk'])
      Like.objects.filter(post=post, profile=profile).delete()
      return redirect('show_post', pk=post.pk)
