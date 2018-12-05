from django.shortcuts import render
from random import randrange
from recommender.views import movie_builder
from movie_query.models import MovieList
from django.http import HttpResponse
import json

# Create your views here.


def get_random(request):

    movie_total = 5000
    movie_number = 9

    response_dict = {'movies': []}
    while len(response_dict['movies']) < movie_number:
        i = randrange(0, movie_total)
        movie_object = MovieList.objects.get(index=i)
        movieId = movie_object.movieid
        movie_dict = movie_builder(str(movieId))
        if movie_dict != 'None':
            response_dict['movies'].append(movie_dict)

    response = json.dumps(response_dict)
    return HttpResponse(response)
