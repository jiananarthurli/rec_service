from django.apps import AppConfig
import pandas as pd
import numpy as np

class RecommenderConfig(AppConfig):
    name = 'recommender'

    def load_movie_sim(self, filename):
        return pd.read_csv(filename, header=0, index_col=0)

    def load_movie_common(self, filename):
        return pd.read_csv(filename, header=0, index_col=0)

    def ready(self):

        beta = 100
        nearest_k = 50

        global movie_sim_beta
        global movie_norm
        global k_nearest

        path = 'data/'

#        movie_sim = pd.read_csv(path + 'UR_weighted_normal_sim.csv', header=0, index_col=0, dtype=np.float32)
        movie_sim = self.load_movie_sim(path + 'UR_weighted_normal_sim.csv')
#        movie_common = pd.read_csv(path + 'UR_common.csv', header=0, index_col=0, dtype=np.int32)
        movie_common = self.load_movie_common(path + 'UR_common.csv')
        movie_sim_beta = movie_sim * (movie_common / (movie_common + beta))
        print("movie_sim_beta loaded")
        movie_norm = movie_sim_beta.apply(abs).sum(axis=1)
        print("movie_norm loaded")

        k_nearest = {}
        for col in movie_sim_beta.columns:
            k_nearest[col] = movie_sim_beta[col].sort_values(ascending=False).index[1:nearest_k + 1]
        print("k_nearest loaded")

