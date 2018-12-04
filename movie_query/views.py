from django.shortcuts import render
import requests
from movie_query.models import MovieList

# Create your views here.


def tmdb_query(tmdbId):
    api_key = '90ad7a0d82f666e2a1946f9a14c64680'
    prefix = 'https://api.themoviedb.org/3/movie/'
    URL = prefix + tmdbId + '?api_key=' + api_key
    r = requests.get(URL).json()
    return r


def tmdb_search(title):
    api_key = '90ad7a0d82f666e2a1946f9a14c64680'
    title_str = title.replace(' ', '+')
    prefix = 'https://api.themoviedb.org/3/search/movie?api_key='
    URL = prefix + api_key + '&query=' + title_str
    r = requests.get(URL).json()
    return str(r['results'][0]['id'])


def get_poster(tmdbId):

    try:
        poster_path = tmdb_query(tmdbId)['poster_path']
    except KeyError:
        movie_object = MovieList.objects.get(tmdbid=tmdbId)
        newId = tmdb_search(movie_object.title)
        poster_path = tmdb_query(newId)['poster_path']

    return 'https://image.tmdb.org/t/p/w500' + poster_path

