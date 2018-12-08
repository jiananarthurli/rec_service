from django.shortcuts import render
import requests
from movie_query.models import MovieList
# from bs4 import BeautifulSoup
# import json
# import re


def tmdb_query(tmdbId):
    api_key = '90ad7a0d82f666e2a1946f9a14c64680'
    prefix = 'https://api.themoviedb.org/3/movie/'
    URL = prefix + tmdbId + '?api_key=' + api_key
    r = requests.get(URL)

    if r.ok:
        return r.json()
    else:
        return 'None'


def tmdb_search(title):
    api_key = '90ad7a0d82f666e2a1946f9a14c64680'
    title_str = title.replace(' ', '+')
    prefix = 'https://api.themoviedb.org/3/search/movie?api_key='
    URL = prefix + api_key + '&query=' + title_str
    r = requests.get(URL).json()
    r_results = r['results']
    if len(r_results) == 0:
        return 'None'
    else:
        return str(r_results[0]['id'])


# def get_poster(tmdbId, poster_size):
def get_tmdb_r(tmdbId, poster_size):

    if tmdbId == 'nan':  # if the tmdbId is nan, especially when get_random is called
        return 'None', 'None'

    if poster_size == 'large':
        size = 'w500'
    elif poster_size == 'small':
        size = 'w185'
    else:
        size = 'w185'

    prefix = 'https://image.tmdb.org/t/p/' + size
    tmdb_r = tmdb_query(tmdbId)

    if tmdb_r != 'None':
        poster_path = tmdb_r['poster_path']

        if poster_path is None:  # this happens when the poster path is None in the tmdb response.
            return 'None', tmdb_r

    else:  # use searching to find the tmdbId instead
        movie_object = MovieList.objects.get(tmdbid=tmdbId)
        movie_title = movie_object.title
        newId = tmdb_search(movie_title)

        if newId == 'None':  # even searching title in tmdb doesn't work
            return 'None', tmdb_r
        else:
            tmdb_r = tmdb_query(newId)
            if tmdb_r == 'None':  # if for any reason the new id could not be found
                return 'None', tmdb_r
            poster_path = tmdb_r['poster_path']

            if poster_path is None:  # this happens when the poster path is None in the tmdb response.
                return 'None', tmdb_r

    # try:
    #     str(poster_path)
    # except TypeError:
    #     return 'None'

    # return prefix + poster_path

    if not isinstance(poster_path, str):
        return 'None', tmdb_r

    return prefix + poster_path, tmdb_r

    #  tmdb_r fields:
    #  'adult',
    #  'backdrop_path',
    #  'belongs_to_collection',
    #  'budget',
    #  'genres',
    #  'homepage',
    #  'id',
    #  'imdb_id',
    #  'original_language',
    #  'original_title',
    #  'overview',
    #  'popularity',
    #  'poster_path',
    #  'production_companies',
    #  'production_countries',
    #  'release_date',
    #  'revenue',
    #  'runtime',
    #  'spoken_languages',
    #  'status',
    #  'tagline',
    #  'title',
    #  'video',
    #  'vote_average',
    #  'vote_count'
