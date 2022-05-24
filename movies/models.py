from django.db import models
from django.conf import settings
# Create your models here.
class Genre(models.Model):
    g_id = models.IntegerField()
    name = models.CharField(max_length=50)
    
class Keyword(models.Model):
    k_id = models.IntegerField()
    name = models.CharField(max_length=100)
    
class Movie(models.Model):
    m_id = models.IntegerField()
    title = models.CharField(max_length=100)
    overview = models.TextField()
    release_date = models.DateField()
    poster_path = models.TextField(null=True)
    backdrop_path = models.TextField(null=True)
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    adult = models.BooleanField(null=True)
    original_language = models.CharField(max_length=50,null=True)
    runtime = models.IntegerField(null=True)
    status = models.CharField(max_length=50,null=True)
    tagline = models.TextField(null=True)
    budget = models.IntegerField()
    revenue = models.IntegerField()
    homepage = models.TextField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    genres = models.ManyToManyField(Genre, through='MovieGenre')
    keywords = models.ManyToManyField(Keyword, through='MovieKeyword')
    now_playing = models.BooleanField(null=True, default=False)
    popular = models.BooleanField(null=True, default=False)
    upcoming = models.BooleanField(null=True, default=False)
    
class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    
class MovieKeyword(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
       
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField()
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')