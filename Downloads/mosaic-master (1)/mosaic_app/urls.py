from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('about-us',about_us, name="about-us"),
    
    path("lang/<str:new_language>/", change_language, name="change-language"),
]