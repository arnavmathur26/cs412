from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

# Create your views here.

def main(request):
   '''Show the main page'''

   template_name = "instagram/main.html"
   return render(request, template_name)


class ProfileListView(ListView):
   '''Show all Profiles'''

   model = Profile
   template_name = "instagram/show_all_profiles.html"
   context_object_name = "profiles"


class ProfileDetailView(DetailView):
   '''Show a single Profile'''

   model = Profile
   template_name = "instagram/show_profile.html"
   context_object_name = "profile"