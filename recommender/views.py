from django.shortcuts import render
from django.http import HttpResponse
from recommender.apps import movie_sim_beta, movie_norm, k_nearest
import json
import pandas as pd


def submit(request):

    rec = 10

    movie_list_str = request.GET['movies']
    picks = movie_list_str.split(',')

    candidate = set()
    for p in picks:
        for i in k_nearest[p].values:
            candidate.add(i)

    # calculate potential ratings of the target user on the candidates
    candidate_index = pd.Index(candidate)
    candidate_rate = movie_sim_beta.loc[candidate_index, picks].sum(axis=1) / movie_norm[candidate_index]

    result = candidate_rate.sort_values(ascending=False).index.values
    recommendations = []
    for i in result:
        if len(recommendations) >= rec:
            break
        if str(int(i)) not in picks:
            recommendations.append(str(int(i)))

    response_dict = {'movies': []}
    for m in recommendations:
        response_dict['movies'].append(
            {'movieId': m}
        )
    response = json.dumps(response_dict)
    return HttpResponse(response)
