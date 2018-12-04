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
