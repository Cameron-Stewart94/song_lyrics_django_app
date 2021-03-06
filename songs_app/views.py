from django.shortcuts import render
from django.views.generic import View, TemplateView
from songs_app.forms import SongChoice, ArtistChoice
from django.http import HttpResponseRedirect, HttpResponse
from songs_app.lyrics_generator import Lyrics
from songs_app.models import Artist, Song
from songs_app.query import random_song_generator, database_check, top_songs_generator
from django.db.models import F

def index(request):
    # View renders the website's index page
    artist_form = ArtistChoice()
    song_form = SongChoice()
    # Initiates instance of form classes

    if request.method == 'POST':
        artist_form = ArtistChoice(data=request.POST)
        song_form = SongChoice(data=request.POST)
        # Checks if forms send post requests and saves form inputs to corresponding variables

        if artist_form.is_valid() and song_form.is_valid():
            # Checks forms are valid and cleans data if they are.
            artist_value = artist_form.cleaned_data['artist']
            song_value = song_form.cleaned_data['song']
            database_information = database_check()
            # Runs database_check function to return lists of artists and songs in the database

            if artist_value.upper() in database_information['artists'] and song_value.upper() in database_information['songs']:
                """Checks if the user input already existis in the database.
                If the user input exists in the database, view returns song inofrmation stored in the database, avoiding scraping the web """

                song_filter = Song.objects.filter(artist__artist__iexact=artist_value).filter(song__iexact=song_value)
                # Filters for searched artist and song, using iexact so the filter fields are case insensitive
                Song.objects.filter(artist__artist__iexact=artist_value).filter(song__iexact=song_value).update(searches=F('searches')+1)
                # If the song exists in the database, the searches field is increased by 1 using F. Default value is 1 for the first time a song is searched.
                return render(request, 'songs_app/lyrics.html', {'artist': song_filter[0].artist, 'song': song_filter[0].song, 'lyrics': song_filter[0].lyrics})

            else:
                web_lyrics = Lyrics(artist_value, song_value)
                # If the user input does not exist in the database, Lyrics instance is created
                try:
                    web_lyrics.fetch_data()
                    # fetch_data function is called to scrape the web
                except:
                    return render(request, 'songs_app/invalid_choice.html')
                    # Renders error page if user input is not valid
                else:
                    song = song_form.save(commit=False)
                    # Saves form input but doesnt commit to database
                    artist, created = Artist.objects.get_or_create(artist = web_lyrics.artist_name)
                    # Uses get_or_create to add artist to database if it doesnt exist already
                    song.lyrics = web_lyrics.song_lyrics
                    song.artist = artist
                    song.song = web_lyrics.song_name
                    case_artist = web_lyrics.artist_name
                    song.save()
                    # Stores artist, song and lyrics in corresponding fields in database
        return render(request, 'songs_app/lyrics.html', {'lyrics': song.lyrics, 'artist': case_artist, 'song': song.song})

    return render(request, 'songs_app/index.html', {'artist_form': artist_form, 'song_form': song_form})


def random_song(request):
    # View displays random song using random_song_generator function in queries.py
    if Song.objects.all():
        random_song = random_song_generator()
        return render(request, 'songs_app/random_song.html', {'artist': random_song['artist'], 'song': random_song['song'], 'lyrics': random_song['lyrics']} )
    else:
        return render(request, 'songs_app/invalid_choice.html', {'no_searches': True})

def top_songs(request):
    number_of_songs = len(Song.objects.all())
    if number_of_songs == 0:
        return render(request, 'songs_app/invalid_choice.html', {'no_searches': True})
    elif number_of_songs > 0 and number_of_songs < 10:
        top_songs = top_songs_generator()
        return render(request, 'songs_app/top_songs.html', {'artist_lst': top_songs['artist_lst'], 'song_lst' : top_songs['song_lst'], 'searches_lst': top_songs['searches_lst'], 'range' : range(number_of_songs)})
    else:
    # Renders top 10 songs to html page
        top_ten_songs = top_songs_generator()
        return render(request, 'songs_app/top_songs.html', {'artist_lst': top_ten_songs['artist_lst'], 'song_lst' : top_ten_songs['song_lst'], 'searches_lst': top_ten_songs['searches_lst'], 'range' : range(10)})


def lyrics(request):
    # Blank lyrics function needed to ensure lyrics.html page is rendered
    pass
