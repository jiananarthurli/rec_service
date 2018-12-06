from django.shortcuts import render
from django.http import HttpResponse
from recommender.apps import movie_sim_beta, movie_norm, k_nearest
import json
import pandas as pd
from movie_query.models import MovieList
from movie_query.views import get_poster


def movie_builder(movieId, poster_size):

    movie_object = MovieList.objects.get(movieid=movieId)
    poster_path = get_poster(movie_object.tmdbid, poster_size)
    if poster_path != 'None':
        result = {'movieId': movieId,
                  'title': movie_object.title,
                  'year': movie_object.year,
                  'imdbId': movie_object.imdbid,
                  'tmdbId': movie_object.tmdbid,
                  'poster': poster_path
                  }
    else:
        result = 'None'

    return result


def submit(request):

    rec = 10

    poster_size = request.GET['size']
    movie_list_str = request.GET['movies']
    if movie_list_str[-1] == ',':
        movie_list_str = movie_list_str[:-1]
    picks = movie_list_str.split(',')

    candidate = set()
    picks = set(picks)

    for p in picks:
        for i in k_nearest[p].values:
            candidate.add(i)

    # calculate potential ratings of the target user on the candidates
    candidate_index = pd.Index(candidate)
    candidate_rate = movie_sim_beta.loc[candidate_index, picks].sum(axis=1) / movie_norm[candidate_index]

    result = candidate_rate.sort_values(ascending=False).index.values

    response_dict = {'movies': []}
    for i in result:
        if len(response_dict['movies']) >= rec:
            break
        if str(int(i)) not in picks:
            m = str(int(i))  # movieId in string
            movie_dict = movie_builder(m, poster_size)
            if movie_dict != 'None':
                response_dict['movies'].append(movie_dict)

    response = json.dumps(response_dict)
    return HttpResponse(response)
