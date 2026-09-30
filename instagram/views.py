from django.shortcuts import render
from django.views.generic import ListView
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