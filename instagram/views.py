from django.shortcuts import render

# Create your views here.

def main(request):
   '''Show the main page'''
   
   template_name = "instagram/main.html"
   return render(request, template_name)