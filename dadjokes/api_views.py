from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer


class RandomJoke(APIView):
    '''
    GET: return a JSON representation of one randomly selected Joke.
    '''

    def get(self, request):
        joke = Joke.objects.order_by('?').first()
        serializer = JokeSerializer(joke)
        return Response(serializer.data)


class JokeList(generics.ListCreateAPIView):
    '''
    GET: return a JSON representation of all Jokes.
    POST: create a new Joke.
    '''

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class JokeDetail(generics.RetrieveAPIView):
    '''
    GET: return a JSON representation of one Joke by its primary key.
    '''

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureList(generics.ListAPIView):
    '''
    GET: return a JSON representation of all Pictures.
    '''

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureDetail(generics.RetrieveAPIView):
    '''
    GET: return a JSON representation of one Picture by its primary key.
    '''

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class RandomPicture(APIView):
    '''
    GET: return a JSON representation of one randomly selected Picture.
    '''

    def get(self, request):
        picture = Picture.objects.order_by('?').first()
        serializer = PictureSerializer(picture)
        return Response(serializer.data)
