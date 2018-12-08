from django.shortcuts import render
from django.http import HttpResponse
from recommender.apps import movie_sim_beta, movie_norm, k_nearest
import json
import pandas as pd
import numpy as np
from movie_query.models import MovieList
from movie_query.views import get_tmdb_r


def movie_builder(movieId, poster_size):

    movie_object = MovieList.objects.get(movieid=movieId)
    poster_path, tmdb_r = get_tmdb_r(movie_object.tmdbid, poster_size)

    if poster_path != 'None':

        try:
            tmdb_title = str(tmdb_r['title'])
        except KeyError:
            tmdb_title = 'NA'

        try:
            imdb_id = str(tmdb_r['imdb_id'])
        except KeyError:
            imdb_id = 'NA'

        try:
            tmdb_runtime = str(tmdb_r['runtime'])
        except KeyError:
            tmdb_runtime = 'NA'

        try:
            tmdb_rating = str(tmdb_r['vote_average'])
        except KeyError:
            tmdb_rating = 'NA'

        try:
            tmdb_overview = str(tmdb_r['overview'])
        except KeyError:
            tmdb_overview = 'NA'

        try:
            genres = build_genres(tmdb_r['genres'])
        except KeyError:
            genres = []

        if tmdb_title == 'NA':
            movie_title = movie_object.title
        else:
            movie_title = tmdb_title

        result = {'movieId': movieId,
                  'title': movie_title,
                  'year': movie_object.year,
                  'runtime': tmdb_runtime,
                  'imdbId': imdb_id,
                  'tmdbId': movie_object.tmdbid,
                  'tmdb_rating': tmdb_rating,
                  'poster': poster_path,
                  'overview': tmdb_overview,
                  'genres': genres
                  }
    else:
        result = 'None'

    return result


def build_genres(genres_list):

    genres = []
    for elem in genres_list:
        genres.append(elem['name'])
    return genres


def submit(request):

    rec = 10  # total number of recommendations returned
    threshold = 0.5

    exclude = set()
    try: # handle the case there exclude is not in the query
        exclude_str = request.GET['exclude']
        if len(exclude_str) > 0 and exclude_str[-1] == ',':
            exclude = set(exclude_str[:-1].split(','))
        else:
            exclude = set(exclude_str.split(','))
    except KeyError:
        pass

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

    # candidate_rate = movie_sim_beta.loc[candidate_index, picks].sum(axis=1) / movie_norm[candidate_index]

    # recommendation with candidate similarity CDF to picks weighted by similarity CDF,
    # within "islands" in picks, and normalized by size of islands: sum(r_cp * r_pp) / count(r_pp)
    cp = movie_sim_beta.loc[candidate_index, picks]
    pp = movie_sim_beta.loc[pd.Index(map(int, picks)), picks]
    # cp_np = cp.values
    # pp_np = pp.values
    # pp_np_filter = pp_np > threshold
    # candidate_rate = pd.Series(np.nanmax(cp_np.dot(pp_np_filter * pp_np) / pp_np_filter.sum(axis=1), axis=1),
    #                            index=cp.index)

    # this is using simple averaging of CDF to get candidate matching
    candidate_rate = cp.mean(axis=1)

    result = candidate_rate.sort_values(ascending=False).index.values

    response_dict = {'movies': []}
    for i in result:
        movieId = str(int(i))
        if len(response_dict['movies']) >= rec:
            break
        if movieId not in picks and movieId not in exclude:
            movie_dict = movie_builder(movieId, poster_size)
            if movie_dict != 'None':
                movie_dict['match'] = str(candidate_rate.loc[i] * 100)
                response_dict['movies'].append(movie_dict)

    response = json.dumps(response_dict)
    return HttpResponse(response)
