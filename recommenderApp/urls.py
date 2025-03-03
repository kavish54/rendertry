from django.urls import path
from . import views

urlpatterns = [
    path('recommend/',views.recomHome,name='recHome'),
    path('logres/',views.loginauth,name='loginauth'),
    path('callback/',views.spotify_callback,name='spotify_callback')
]