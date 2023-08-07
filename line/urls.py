from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('send', send),
    path('sendImage', sendImage),
]

