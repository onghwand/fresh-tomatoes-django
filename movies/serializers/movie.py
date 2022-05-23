from rest_framework import serializers
from ..models import Movie, Genre, Keyword

class MovieListSerializer(serializers.ModelSerializer):
       
    class Meta:
        model = Movie
        fields = ('pk', 'title', 'poster_path', 'like_users',)
        
        
class MovieSerializer(serializers.ModelSerializer):
    
    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = ('pk', 'name')
    
    class KeywordSerializer(serializers.ModelSerializer):
        class Meta:
            model = Keyword
            fields = ('pk', 'name')
    
    genres = GenreSerializer(many=True)
    keywords = KeywordSerializer(many=True)
    
    class Meta:
        model = Movie
        fields = '__all__'
        
class MovieReleaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ('pk', 'title', 'release_date', 'popularity', 'poster_path', 'like_users',)

class MovieGenreSerializer(serializers.ModelSerializer):
    
    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = ('pk', 'name')
    genres = GenreSerializer(many=True)   
       
    class Meta:
        model = Movie
        fields = ('pk', 'title', 'genres', 'poster_path', 'like_users',)