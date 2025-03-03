from django.shortcuts import render,redirect
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

os.environ['SPOTIPY_CLIENT_ID'] = 'cfd82609829c4df08e69069c5c37e201'
os.environ['SPOTIPY_CLIENT_SECRET'] = '0cc553a74abf4a328b0cd70a661fd01f'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:8000/callback'

# Create your views here.

def recomHome(request):
    return render(request,'recommenderApp/recomm.html',context = {})


def loginauth(request):
    scope = "user-library-read"
    auth = SpotifyOAuth(scope=scope)

    auth_url = auth.get_authorize_url()

    return redirect(auth_url)

def spotify_callback(request):
    auth = SpotifyOAuth(scope="user-library-read")
    
    # Get authorization code from URL parameters
    code = request.GET.get("code")

    if "spotify_token" in request.session:
        del request.session["spotify_token"]
    
    if code:
        # Exchange authorization code for access token
        token_info = auth.get_access_token(code)
        
        # Save token in session (optional)
        # request.session["spotify_token"] = token_info

        sp = spotipy.Spotify(auth=token_info["access_token"])
        user = sp.current_user()
        playlists = sp.current_user_playlists()
        
        context = {
            'token':token_info,
            'user':user,
            'playlist':playlists
        }
        print(playlists)
        return render(request,'recommenderApp/logres.html',context)  # Redirect to logres page after successful login
    # else:
    #     return render(request,'recommenderApp/logres.html',context = {})