from rest_framework import serializers
from ..models import Movie, Genre, Keyword

class MovieListSerializer(serializers.ModelSerializer):
    
    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = ('name',)
            
    genres = GenreSerializer(many=True)
    
    class Meta:
        model = Movie
        fields = ('pk', 'title', 'poster_path', 'like_users', 'tagline', 'release_date', 'overview', 'popularity', 'runtime', 'genres',)
        
        
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
        fields = ('pk', 'title', 'release_date', 'popularity', 'poster_path', 'like_users', 'runtime',)

class MovieGenreSerializer(serializers.ModelSerializer):
    
    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = ('pk', 'name')
    genres = GenreSerializer(many=True)   
       
    class Meta:
        model = Movie
        fields = ('pk', 'title', 'genres', 'poster_path', 'like_users', 'runtime',)
        
class QuestionsSerializer(serializers.ModelSerializer):
    
    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = ('pk', 'name')
    genres = GenreSerializer(many=True)  
    
    class Meta:
        model = Movie
        fields = ('pk', 'title', 'genres', 'poster_path', 'like_users', 'release_date', 'runtime', 'popularity')