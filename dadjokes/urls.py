#dadjokes/urls.py

from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('', views.random_page, name='dadjokes_home'),
    path('random', views.random_page, name='random'),
    path('jokes', views.show_all_jokes, name='show_all_jokes'),
    path('joke/<int:pk>', views.show_joke, name='show_joke'),
    path('pictures', views.show_all_pictures, name='show_all_pictures'),
    path('picture/<int:pk>', views.show_picture, name='show_picture'),

    # REST API
    path('api/', api_views.RandomJoke.as_view(), name='api_home'),
    path('api/random', api_views.RandomJoke.as_view(), name='api_random_joke'),
    path('api/jokes', api_views.JokeList.as_view(), name='api_jokes'),
    path('api/joke/<int:pk>', api_views.JokeDetail.as_view(), name='api_joke'),
    path('api/pictures', api_views.PictureList.as_view(), name='api_pictures'),
    path('api/picture/<int:pk>', api_views.PictureDetail.as_view(), name='api_picture'),
    path('api/random_picture', api_views.RandomPicture.as_view(), name='api_random_picture'),
]
