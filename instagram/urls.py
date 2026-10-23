# urls.py defines the url routing for the instagram app
# It maps the root path (r'') to ProfileListView to show all profiles,
# and 'profile/<int:pk>' to ProfileDetailView to show a single profile

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path(r'', views.ProfileListView.as_view(), name="show_all_profiles"),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), ## NEW
	path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'), ## NEW

    path('profile', views.ShowMyProfileView.as_view(), name="profile"),
    path('profile/create_post', views.CreatePostView.as_view(), name="create_post"),
    path('profile/update', views.UpdateProfileView.as_view(), name="update_profile"),
    path('profile/feed', views.ShowFeedView.as_view(), name="show_feed"),
    path('profile/search', views.SearchView.as_view(), name="search"),

    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name="show_my_profile"),
    path('profile/<int:pk>/followers', views.ShowFollowersDetailView.as_view(), name="show_followers"),
    path('profile/<int:pk>/following', views.ShowFollowingDetailView.as_view(), name="show_following"),

    path('post/<int:pk>', views.PostDetailView.as_view(), name="show_post"),
    path('post/<int:pk>/delete', views.DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update', views.UpdatePostView.as_view(), name="update_post"),
]
