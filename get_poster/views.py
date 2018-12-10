from django.shortcuts import render
from django.http import HttpResponse


def poster_small(request, filename):

    path = 'data/posters/w185/'
    image_path = path + filename
    with open(image_path, "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")


def poster_large(request, filename):

    path = 'data/posters/w500/'
    image_path = path + filename
    with open(image_path, "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")