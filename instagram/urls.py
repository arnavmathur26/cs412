# urls.py defines the url routing for the instagram app
# It maps the root path (r'') to ProfileListView to show all profiles

from django.urls import path
from . import views


urlpatterns = [
    path(r'', views.ProfileListView.as_view(), name="show_all_profiles"),
]
