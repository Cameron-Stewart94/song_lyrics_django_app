from django.shortcuts import render
from django.views.generic import View, TemplateView
from songs_app.forms import SongChoice, ArtistChoice
from django.http import HttpResponseRedirect, HttpResponse
from songs_app.lyrics_generator import Lyrics
from songs_app.models import Artist, Song

# Create your views here.
def index(request):
    artist_form = ArtistChoice()
    song_form = SongChoice()


    if request.method == 'POST':
        artist_form = ArtistChoice(data=request.POST)
        song_form = SongChoice(data=request.POST)

        if artist_form.is_valid() and song_form.is_valid():
            artist_value = artist_form.cleaned_data['artist']
            song_value = song_form.cleaned_data['song']
            web_lyrics = Lyrics(artist_value, song_value)
            try:
                web_lyrics.fetch_data()
            except:
                return render(request, 'songs_app/invalid_choice.html')
            else:
                song = song_form.save(commit=False)
                artist, created = Artist.objects.get_or_create(artist = web_lyrics.artist_name)
                song.lyrics = web_lyrics.song_lyrics
                song.artist = artist
                song.song = web_lyrics.song_name
                case_artist = web_lyrics.artist_name

                try:
                    song.save()
                except:
                    return render(request, 'songs_app/lyrics.html', {'lyrics': song.lyrics, 'artist': case_artist, 'song': song.song})

        return render(request, 'songs_app/lyrics.html', {'lyrics': song.lyrics, 'artist': case_artist, 'song': song.song})


    else:
        print('Invalid Information Provided')
    return render(request, 'songs_app/index.html', {'artist_form': artist_form, 'song_form': song_form})

def lyrics(request):
    return render(request, 'songs_app/lyrics.html')
