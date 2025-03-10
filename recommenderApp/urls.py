from django.urls import path
from . import views

urlpatterns = [
    path('recommend/',views.recomHome,name='recHome'),
    path('logres/',views.loginauth,name='loginauth'),
    path('callback/',views.spotify_callback,name='spotify_callback'),
    path("autocomplete/", views.spotify_autocomplete, name="spotify-autocomplete"),
    path("results/<str:sid>/",views.show_recommendations,name="recResult")
]