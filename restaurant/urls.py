#urls.py defines the url routing for the resturaunt app
#It maps the three paths, main (r''), order, and submit to view functions

from django.urls import path
from django.conf import settings
from . import views


urlpatterns = [
    path(r'', views.main, name="main"),
    path(r'order/', views.order, name="order"),
    path(r'submit', views.submit, name="submit"),

]

