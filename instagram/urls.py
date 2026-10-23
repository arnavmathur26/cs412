# urls.py defines the url routing for the instagram app
# It maps the root path (r'') to ProfileListView to show all profiles,
# and 'profile/<int:pk>' to ProfileDetailView to show a single profile

from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path(r'', views.ProfileListView.as_view(), name="show_all_profiles"),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), ## NEW
	path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('logout_confirmation')), name='logout'), ## NEW
	path('logout_confirmation/', views.LogoutConfirmationView.as_view(), name='logout_confirmation'), ## NEW

    path('create_profile', views.CreateProfileView.as_view(), name="create_profile"),
    path('profile', views.ShowMyProfileView.as_view(), name="profile"),
    path('profile/create_post', views.CreatePostView.as_view(), name="create_post"),
    path('profile/update', views.UpdateProfileView.as_view(), name="update_profile"),
    path('profile/feed', views.ShowFeedView.as_view(), name="show_feed"),
    path('profile/search', views.SearchView.as_view(), name="search"),

    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name="show_my_profile"),
    path('profile/<int:pk>/followers', views.ShowFollowersDetailView.as_view(), name="show_followers"),
    path('profile/<int:pk>/following', views.ShowFollowingDetailView.as_view(), name="show_following"),
    path('profile/<int:pk>/follow', views.FollowProfileView.as_view(), name="follow_profile"),
    path('profile/<int:pk>/delete_follow', views.DeleteFollowProfileView.as_view(), name="delete_follow_profile"),

    path('post/<int:pk>', views.PostDetailView.as_view(), name="show_post"),
    path('post/<int:pk>/delete', views.DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update', views.UpdatePostView.as_view(), name="update_post"),
    path('post/<int:pk>/like', views.LikePostView.as_view(), name="like_post"),
    path('post/<int:pk>/delete_like', views.DeleteLikePostView.as_view(), name="delete_like_post"),
]
