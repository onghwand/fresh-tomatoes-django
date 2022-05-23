from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Review

User = get_user_model()

class ReviewSerializer(serializers.ModelSerializer):
    
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('pk', 'username')

    user = UserSerializer(read_only=True)
    like_users = UserSerializer(read_only=True, many=True)
    
    class Meta:
        model = Review
        fields = ('pk', 'user', 'content', 'movie', 'score', 'like_users')
        read_only_fields = ('movie', )
