from django.shortcuts import render, redirect
import random


# Create your views here.

specials = [
    "Durr BLT",
    "Triple Quarter Pounder",
    "Big Bertha",
    "Pulled Pork Sandwich",
]

prices = {
    "Durr Burger": 8.00,
    "Cheeseburger": 9.00,
    "Veggie Burger": 8.50,
    "Chicken Sandwich": 8.50,
    "Special": 12.00,
    "Fries": 5.00,
    "Onion Rings": 6.00,
    "No Side": 0.00,
    "Water": 2.00,
    "Soda": 3.00,
    "Lemonade": 2.50,
}

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
    context = {
        "special": random.choice(specials)
    }
    return render(request, template_name, context)

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

        total_price = 0.00
        for item in entrees + side + drink:
            total_price += prices.get(item, 0)
        total_price = round(total_price, 2)
        context = {
            'name': name,
            'email': email,
            'phone': phone,
            'entrees': entrees,
            'side': side,
            'drink': drink,
            'instructions': instructions,
            'total': total_price,
        }

        return render(request, template_name, context=context)

    # nothing was submitted, so send the user back to the form
    return redirect('order')
