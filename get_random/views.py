from django.shortcuts import render
from random import randrange, uniform
from recommender.views import movie_builder
from movie_query.models import MovieList, MovieRatingsSelected
from django.http import HttpResponse
import json
from django.db.models import Max, Min
from django.core.exceptions import MultipleObjectsReturned


def get_random(request):

    movie_number = 9

    exclude = set()
    try:
        exclude_str = request.GET['exclude']
        if len(exclude_str) > 0 and exclude_str[-1] == ',':
            exclude = set(exclude_str[:-1].split(','))
        else:
            exclude = set(exclude_str.split(','))
    except KeyError:
        pass

    max_weight_c = MovieRatingsSelected.objects.all().aggregate(Max('weight_c'))['weight_c__max']

    response_dict = {'movies': []}
    included = set()
    while len(response_dict['movies']) < movie_number:
        weight_c_random = randrange(0, max_weight_c)
        movie_weight_c = MovieRatingsSelected.objects.filter(weight_c__gte=weight_c_random).aggregate(Min('weight_c'))['weight_c__min']

        try:
            movie_object = MovieRatingsSelected.objects.get(weight_c=movie_weight_c)
        except MultipleObjectsReturned:
            continue

        movieId = str(movie_object.movieid)
        movie_dict = movie_builder(movieId, poster_size='small')
        if movie_dict != 'None' and movieId not in included and movieId not in exclude:
            response_dict['movies'].append(movie_dict)
            included.add(movieId)

    response = json.dumps(response_dict)
    return HttpResponse(response)
