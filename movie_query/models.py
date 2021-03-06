from django.db import models


class MovieList(models.Model):
    index = models.BigIntegerField(blank=False, null=False)
    movieid = models.BigIntegerField(primary_key=True, db_column='movieId', blank=False, null=False)  # Field name made lowercase.
    title = models.TextField(blank=True, null=True)
    genres = models.TextField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)
    imdbid = models.TextField(db_column='imdbId', blank=True, null=True)  # Field name made lowercase.
    tmdbid = models.TextField(db_column='tmdbId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'movie_list'


class MovieRatingsSelected(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    movieid = models.BigIntegerField(primary_key=True, db_column='movieId', blank=True, null=False)  # Field name made lowercase.
    ratings = models.BigIntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    weight_c = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_ratings_selected'


class MoviePosters(models.Model):
    movieid = models.BigIntegerField(db_column='movieId', primary_key=True)  # Field name made lowercase.
    filename = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_posters'


class MovieImdbRating(models.Model):
    movieid = models.BigIntegerField(primary_key=True, db_column='movieId', blank=True, null=False)  # Field name made lowercase.
    imdb_rating = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_imdb_rating'
