from django.shortcuts import render
import requests
# Create your views here.


def tmdb_query(tmdbId):
    api_key = '90ad7a0d82f666e2a1946f9a14c64680'
    prefix = 'https://api.themoviedb.org/3/movie/'
    URL = prefix + tmdbId + '?api_key=' + api_key
    r = requests.get(URL).json()
    return r


def get_poster(tmdbId):
    try:
        poster_path = tmdb_query(tmdbId)['poster_path']
        return 'https://image.tmdb.org/t/p/w500/' + poster_path
    except KeyError:
        return 'None'
