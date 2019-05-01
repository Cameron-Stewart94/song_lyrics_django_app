from songs_app.models import Artist, Song
from random import randint
from collections import defaultdict

def random_song_generator():
    # Function generates a random song from database
    song_query = Song.objects.all()
    number_of_songs = len(song_query)
    random_number = randint(0, number_of_songs - 1)
    artist = song_query[random_number].artist
    song = song_query[random_number].song
    lyrics = song_query[random_number].lyrics
    return {'artist': artist, 'song': song, 'lyrics': lyrics}

def top_song():
    artist_info = Artist.objects.all()
    song_info = Song.objects.all()
    artist_lst =[]
    song_lst = []
    for i in range(len(artist_info)):
        artist_lst.append(str(artist_info[i].artist).upper())

    for i in range(len(song_info)):
        song_lst.append(str(song_info[i].song).upper())



    return {'artists': artist_lst, 'songs': song_lst}
