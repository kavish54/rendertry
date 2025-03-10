from django.shortcuts import render,redirect
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth,SpotifyClientCredentials
from django.http import JsonResponse

os.environ['SPOTIPY_CLIENT_ID'] = 'cfd82609829c4df08e69069c5c37e201'
os.environ['SPOTIPY_CLIENT_SECRET'] = '0cc553a74abf4a328b0cd70a661fd01f'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:8000/callback'

# Create your views here.

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id='cfd82609829c4df08e69069c5c37e201',
        client_secret='0cc553a74abf4a328b0cd70a661fd01f'
    )
)

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

def spotify_autocomplete(request):
    query = request.GET.get("q",'')
    if not query:
        return JsonResponse({"Error":"No query provided"},status=400)
    results = sp.search(q=query, type="track", limit=5)

    suggestions = []
    for item in results["tracks"]["items"]:
        suggestions.append({
            "id": item["id"],
            "name": item["name"],
            "artist": item["artists"][0]["name"],
            "album": item["album"]["name"],
            "image": item["album"]["images"][0]["url"] if item["album"]["images"] else "",
            "spotify_url": item["external_urls"]["spotify"]
        })

    return JsonResponse({"suggestions": suggestions})

def show_recommendations(request,sid):
    context = {
        "sid" : sid 
    }
    recs = sp.audio_features(tracks=[sid])
    for track in recs['tracks']:
        print(f"Track name: {track['name']}")
        print(f"Artist: {track['artists'][0]['name']}")
        print(f"URL: {track['external_urls']['spotify']}")
        print("------")
    return render(request,'recommenderApp/recom-result.html',context=context)