from django.shortcuts import render
from random import randrange, uniform, shuffle
from recommender.views import movie_builder, get_rec
from movie_query.models import MovieList, MovieRatingsSelected
from django.http import HttpResponse
import json
from django.db.models import Max, Min
from django.core.exceptions import MultipleObjectsReturned
from numpy import cumsum, searchsorted, exp


def get_random(request):

    movie_number = 9
    database_size = 5000
    rate_magnifier = 100000
    rec_size_factor = 20
    rank_factor = -0.05

    exclude = set()
    try:
        exclude_str = request.GET['exclude']
        if len(exclude_str) > 0 and exclude_str[-1] == ',':
            exclude = set(exclude_str[:-1].split(','))
        else:
            exclude = set(exclude_str.split(','))
    except KeyError:
        pass

    picks = set()
    try:
        picks_str = request.GET['picks']
        if len(picks_str) > 0:  # consider the case for "&picks="
            if picks_str[-1] == ',':
                picks = set(picks_str[:-1].split(','))
            else:
                picks = set(picks_str.split(','))
    except KeyError:
        pass

    rec = []
    if len(picks) > 0:
        rec = get_rec(picks)
        rec = rec.reset_index()  # fields: movieId, rate, match
        rec.columns = ['movieId', 'rate', 'match']
        rec['movieId'] = rec['movieId'].apply(str)

        # rate_weighted_cumsum is calculated by damping the rate with rank factor, exp(rank * rank_factor),
        # then times rate_magnifier and convert to integer for easy sampling
        rec['rate_weighted_cumsum'] = cumsum((rec['rate'] * exp(rank_factor * rec.index.values) * rate_magnifier).apply(int).values)
        # print((rec['rate'] * exp(rank_factor * rec.index.values) * rate_magnifier).apply(int).values)
        max_rate_cumsum = rec['rate_weighted_cumsum'].iloc[-1]

    rec_size = len(rec)
    # ratio from_rec : from_random = rec_size * rec_size_factor : database_size.
    # If rec_size * rec_size_factor  > database_size, then all movies are from rec
    # Typical rec_size is several hundreds
    from_rec = min(int(movie_number * rec_size * rec_size_factor / database_size), movie_number)

    response_dict = {'movies': []}
    included = set()

    # get movies from recommendations, weight by rate
    while len(response_dict['movies']) < from_rec:

        rate_cumsum_random = uniform(0, max_rate_cumsum)
        movieId = rec['movieId'].iloc[searchsorted(rec['rate_weighted_cumsum'].values, rate_cumsum_random)]
        movie_dict = movie_builder(movieId, poster_size='small')
        if movie_dict != 'None' and movieId not in included and movieId not in exclude and movieId not in picks:
            response_dict['movies'].append(movie_dict)
            included.add(movieId)

    # get movies from the db, weight by weight
    max_weight_c = MovieRatingsSelected.objects.all().aggregate(Max('weight_c'))['weight_c__max']

    while len(response_dict['movies']) < movie_number:

        weight_c_random = randrange(0, max_weight_c)
        movie_weight_c = MovieRatingsSelected.objects.filter(weight_c__gte=weight_c_random).aggregate(Min('weight_c'))['weight_c__min']

        try:
            movie_object = MovieRatingsSelected.objects.get(weight_c=movie_weight_c)
        except MultipleObjectsReturned:
            continue

        movieId = str(movie_object.movieid)
        movie_dict = movie_builder(movieId, poster_size='small')
        if movie_dict != 'None' and movieId not in included and movieId not in exclude and movieId not in picks:
            response_dict['movies'].append(movie_dict)
            included.add(movieId)

    # mix the movies from random pick and movies from get_rec
    shuffle(response_dict['movies'])

    response_dict['source'] = {"rec": str(from_rec),
                               "random": str(movie_number - from_rec)
                               }

    response = json.dumps(response_dict)
    return HttpResponse(response)

