
from rest_framework import serializers
from django.contrib.auth import get_user_model
from movies.models import Movie, Review
# like movies랑 comments 가져와야함

class ProfileSerializer(serializers.ModelSerializer):
    
    class MovieSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Movie
            fields = '__all__'
            
    class ReviewSerializer(serializers.ModelSerializer):
        
        class MovieSerializer(serializers.ModelSerializer):
        
            class Meta:
                model = Movie
                fields = ('pk','title','poster_path')
                
        movie = MovieSerializer()
        
        class Meta:
            model = Review
            fields = '__all__'
            
    like_movies = MovieSerializer(many=True)
    reviews = ReviewSerializer(many=True)
            
    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'email', 'like_movies', 'reviews')