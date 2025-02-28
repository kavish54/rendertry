from django.shortcuts import redirect, render
from django.contrib.auth.models import User
import librosa
from .forms import UploadSongForm
from .feature_extraction.feature_extraction import feature_extract,convert_to_wav,genre_finder 

# Create your views here.

def genreHome(request):
    if request.method == "POST":
        form = UploadSongForm(request.POST, request.FILES)
        if form.is_valid():
            song_obj = form.save(commit=False)
            song_obj.user = User.objects.get(username="admin")
            song_obj.name = song_obj.file.name

            song_obj.save()
            
            # Convert and Extract Features
            file_path = song_obj.file.path
            wav_path = convert_to_wav(file_path)  # Convert to WAV
            song, sr = librosa.load(wav_path, sr=None)
            features = feature_extract(song, sr)

            genre = genre_finder(features)

            # Save extracted features
            for key, value in features.items():
                setattr(song_obj, key, value)

            song_obj.genre = genre
            song_obj.duration = len(song) / 1000
            song_obj.save()  # Save to DB
            
            return render(request, "genreApp/genre-result.html", {"song": song_obj})

    else:
        form = UploadSongForm()
    return render(request,'genreApp/genre-home.html')