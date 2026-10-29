# urls.py defines the url routing for the voter_analytics app

from django.urls import path

from . import views

urlpatterns = [
    path('', views.VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>', views.VoterDetailView.as_view(), name='voter'),
]
