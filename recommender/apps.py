from django.apps import AppConfig
import pandas as pd
import numpy as np

class RecommenderConfig(AppConfig):
    name = 'recommender'



    def ready(self):

        # beta = 100
        nearest_k = 50

        def load_movie_sim(filename):
            return pd.read_csv(filename, header=0, index_col=0)

        # def load_movie_common(filename):
        #     return pd.read_csv(filename, header=0, index_col=0)
        #
        # def to_CDF(i):
        #     return (np.searchsorted(movie_sim_np_row, i, side='right') / movie_sim_np_row.size - 0.5) * 2

        global movie_sim_beta
        global movie_norm
        global k_nearest

        path = 'data/'

        # movie_sim = load_movie_sim(path + 'UR_weighted_normal_sim.csv')
        #
        # movie_sim_np = movie_sim.values
        # movie_sim_np_row = movie_sim_np.reshape(1, movie_sim.shape[0] ** 2)
        # movie_sim_np_row.sort()
        # movie_sim_np_row = movie_sim_np_row[~np.isnan(movie_sim_np_row)]

        # this makes the similarity to be CDF of similarity
        # movie_sim = movie_sim.apply(to_CDF)

        # movie_common = load_movie_common(path + 'UR_common.csv')
        # movie_sim_beta = movie_sim * (movie_common / (movie_common + beta))

        movie_sim_beta = load_movie_sim(path + 'UR_weighted_normal_sim_CDF_beta.csv')
        print("movie_sim_beta loaded")
        movie_norm = movie_sim_beta.apply(abs).sum(axis=1)
        print("movie_norm loaded")

        k_nearest = {}
        for col in movie_sim_beta.columns:
            k_nearest[col] = movie_sim_beta[col].sort_values(ascending=False).index[1:nearest_k + 1]
        print("k_nearest loaded")

