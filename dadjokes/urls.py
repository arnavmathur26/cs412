#dadjokes/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.random_page, name='dadjokes_home'),
    path('random', views.random_page, name='random'),
    path('jokes', views.show_all_jokes, name='show_all_jokes'),
    path('joke/<int:pk>', views.show_joke, name='show_joke'),
    path('pictures', views.show_all_pictures, name='show_all_pictures'),
    path('picture/<int:pk>', views.show_picture, name='show_picture'),
]
