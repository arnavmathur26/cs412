from .serializers import PostsSerializer, ProfileSerializer
from .models import Photo, Posts, Profile
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class LoginView(ObtainAuthToken):
    '''
    POST username/password: return an auth token plus the logged-in User's Profile id.
    '''

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        profile = Profile.objects.filter(user=user).first()
        return Response({
            'token': token.key,
            'profile_id': profile.pk if profile else None,
        })

class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetail(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class PostsByProfile(generics.ListCreateAPIView):
    serializer_class = PostsSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return profile.get_posts()

    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        if profile.user != self.request.user:
            raise PermissionDenied("You can't create a post for another user's profile.")
        post = serializer.save(profile=profile)
        for file in self.request.FILES.getlist('files'):
            Photo.objects.create(post=post, image_file=file)

class ProfileFeed(generics.ListAPIView):
    serializer_class = PostsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        if profile.user != self.request.user:
            raise PermissionDenied("You can't view another user's feed.")
        return profile.get_post_feed()
