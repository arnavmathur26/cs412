from django.shortcuts import render, redirect


# Create your views here.

def main(request):
   '''Show the main page for Durr Burger resturaunt'''
   context = {
       'image': "images/durr_burger.webp",
   }
   template_name = "restaurant/main.html"
   return render(request, template_name, context)



def order(request):
    '''Show the web page with the order form.'''

    template_name = "restaurant/order.html"
    return render(request, template_name)

def submit(request):
    '''Process the form submission, and generate a result.'''

    template_name = "restaurant/confirmation.html"

    # read the form data into python variables:
    if request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        entrees = request.POST.getlist('entrees')
        side = request.POST.getlist('side')
        drink = request.POST.getlist('drink')
        instructions = request.POST.get('instructions')

        context = {
            'name': name,
            'email': email,
            'phone': phone,
            'entrees': entrees,
            'side': side,
            'drink': drink,
            'instructions': instructions,
        }

        return render(request, template_name, context=context)

    # nothing was submitted, so send the user back to the form
    return redirect('order')
