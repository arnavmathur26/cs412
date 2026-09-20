import random

from django.shortcuts import render

# Create your views here.

#Tom brady quotes
quotes = [
    "You wanna know which ring is my favorite? The next one.",
    "If you don't believe in yourself why is anyone else going to believe in you?",
    "Every quarterback can throw a ball; every running back can run; every receiver is fast; but that mental toughness that you talk about translates into competitiveness.",
    "If you don't play to win, don't play at all.",
    "To be successful at anything, the truth is you don’t have to be special. You just have to be what most people aren’t: consistent, determined and willing to work for it"

]
#Tom brady images
images = [
    "images/brady1.jpg",
    "images/brady2.jpg",
    "images/brady3.jpeg",
    "images/brady4.jpg",
]

#Gets random quote and imagefrom quotes list
def quote(request):
    '''
    Show one randomly selected quote and image.
    '''

    context = {
        'quote': random.choice(quotes),
        'image': random.choice(images),
    }
    return render(request, 'quote/quote.html', context)

#Gets all quotes and images
def show_all(request):
    '''
    Show all quotes and all images.
    '''

    context = {
        'quotes': quotes,
        'images': images,
    }
    return render(request, 'quote/show_all.html', context)

def about(request):
    '''
    Show biographical information about Tom Brady and the app.
    '''

    return render(request, 'quote/about.html')
