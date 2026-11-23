from .serializers import PostsSerializer, ProfileSerializer
from .models import Photo, Posts, Profile
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetail(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class PostsByProfile(generics.ListCreateAPIView):
    serializer_class = PostsSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return profile.get_posts()

    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        post = serializer.save(profile=profile)
        for file in self.request.FILES.getlist('files'):
            Photo.objects.create(post=post, image_file=file)

class ProfileFeed(generics.ListAPIView):
    serializer_class = PostsSerializer

    def get_queryset(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return profile.get_post_feed()
    