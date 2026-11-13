from django.shortcuts import render, get_object_or_404

from .models import Joke, Picture

# Create your views here.


def random_page(request):
    '''
    Show one randomly selected Joke and one randomly selected Picture.
    '''

    context = {
        'joke': Joke.objects.order_by('?').first(),
        'picture': Picture.objects.order_by('?').first(),
    }
    return render(request, 'dadjokes/random.html', context)


def show_all_jokes(request):
    '''
    Show a page with all Jokes (no images).
    '''

    context = {
        'jokes': Joke.objects.all(),
    }
    return render(request, 'dadjokes/show_all_jokes.html', context)


def show_joke(request, pk):
    '''
    Show one Joke by its primary key.
    '''

    context = {
        'joke': get_object_or_404(Joke, pk=pk),
    }
    return render(request, 'dadjokes/show_joke.html', context)


def show_all_pictures(request):
    '''
    Show a page with all Pictures (no jokes).
    '''

    context = {
        'pictures': Picture.objects.all(),
    }
    return render(request, 'dadjokes/show_all_pictures.html', context)


def show_picture(request, pk):
    '''
    Show one Picture by its primary key.
    '''

    context = {
        'picture': get_object_or_404(Picture, pk=pk),
    }
    return render(request, 'dadjokes/show_picture.html', context)
