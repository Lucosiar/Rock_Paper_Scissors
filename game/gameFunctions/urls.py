# juego/urls.py

from django.urls import path
from .views import home, play, correct_move_view

urlpatterns = [
    path('', home, name='home'),
    path('play/', play, name='play'),
    path('correctTheMove/', correct_move_view, name='correctTheMove'),
]