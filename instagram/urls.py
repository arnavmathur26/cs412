# urls.py defines the url routing for the instagram app
# It maps the root path (r'') to ProfileListView to show all profiles,
# and 'profile/<int:pk>' to ProfileDetailView to show a single profile

from django.urls import path
from . import views


urlpatterns = [
    path(r'', views.ProfileListView.as_view(), name="show_all_profiles"),
    path(r'profile/<int:pk>', views.ProfileDetailView.as_view(), name="show_profile"),
    path('profile/create', views.CreatePostView.as_view(), name="create_profile"),
    path('post/<int:pk>', views.PostDetailView.as_view(), name="show_post"),
]
