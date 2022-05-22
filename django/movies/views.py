import requests
import datetime
from django.shortcuts import get_list_or_404, get_object_or_404

from .serializers.movie import MovieListSerializer, MovieSerializer, MovieReleaseSerializer
from .serializers.review import ReviewSerializer
from .models import Movie, MovieGenre, Genre, Review, Keyword, MovieKeyword
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status

#import json

BASE_URL = 'https://api.themoviedb.org/3'

@api_view(['GET'])
def movie(request):
    movies = get_list_or_404(Movie)
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

    
@api_view(['POST'])
def like_movie(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user
    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        serializer = MovieListSerializer(movie)
        return Response(serializer.data)
    else:
        movie.like_users.add(user)
        serializer = MovieListSerializer(movie)
        return Response(serializer.data)
    
@api_view(['GET']) 
def related_genre(request, movie_pk): # 해당 영화가 가진 장르들과 똑같은 장르를 포함한 영화들 , 평점순으로 order_by해서 상위 5개 뽑을까 나중에 수정하기
    movie = get_object_or_404(Movie, pk=movie_pk)
    moviegenres = MovieGenre.objects.filter(movie_id=movie.pk)
    pass

@api_view(['GET']) 
def related_release_date(request, movie_pk): # 해당 영화 개봉일 앞뒤 7일 이내에 개봉한 영화들
    movie = get_object_or_404(Movie, pk=movie_pk)
    #print(movie.release_date, type(movie.release_date))
    #release_date = datetime.datetime.strptime(movie.release_date, "%Y-%m-%d")
    start_date = movie.release_date - datetime.timedelta(days=7)
    end_date = movie.release_date + datetime.timedelta(days=7)
    
    movies = Movie.objects.filter(release_date__range=(start_date, end_date)).order_by("-popularity")
    serializer = MovieReleaseSerializer(movies, many=True)
    return Response(serializer.data)
    


@api_view(['GET','POST'])
def review_read_or_create(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    def read_review():
        reviews = movie.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    def create_review():
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=user)
            
            reviews = movie.reviews.all()
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    if request.method == 'GET':
        return read_review()
    elif request.method == 'POST':
        return create_review()
    
@api_view(['PUT', 'DELETE'])
def review_update_or_delete(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    
    def update_review():
        if request.user == review.user:
            serializer = ReviewSerializer(instance=review, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                reviews = movie.reviews.all()
                serializer = ReviewSerializer(reviews, many=True)
                return Response(serializer.data)
    
    def delete_review():
        if request.user == review.user:
            review.delete()
            reviews = movie.reviews.all()
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)
    
    if request.method == 'PUT':
        return update_review()
    elif request.method == 'DELETE':
        return delete_review()
    
@api_view(['POST'])
def like_review(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    #review = get_object_or_404(Review, pk=review_pk)
    review = movie.reviews.get(pk=review_pk)
    user = request.user
    
    if review.like_users.filter(pk=user.pk).exists():
        review.like_users.remove(user)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    else:
        review.like_users.add(user)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
 
@api_view(['GET']) 
def now_playing(request): # 시간이 너무 오래 걸림.. table을 따로 만드는게 맞는가 싶음
    path_now_playing = '/movie/now_playing'
    
    params = {
            'api_key' : '1c495200bf8a0c1956a9c60b7877da9c',
            'language' : 'en-US',
        }
    params_keywords = {
        'api_key' : '1c495200bf8a0c1956a9c60b7877da9c',
    }
    # 전체 영화 다 False로 초기화
    movies = get_list_or_404(Movie)
    for movie in movies:
        movie.now_playing = False
        movie.save()
    
    # 상영중인 영화를 받아옴  
    response_now_playing = requests.get(BASE_URL+path_now_playing, params=params).json()['results']
    for response in response_now_playing:
        if not Movie.objects.filter(m_id=response['id']).exists():
            movie_id = response['id']
            path_detail = f'/movie/{movie_id}'
            path_keywords = f'/movie/{movie_id}/keywords'
            detail = requests.get(BASE_URL+path_detail, params=params).json()
            keywords = requests.get(BASE_URL+path_keywords, params=params_keywords).json()
            
            movie = Movie.objects.create(m_id=detail['id'],
                                        title=detail['title'],
                                        overview=detail['overview'],
                                        release_date=detail['release_date'],
                                        poster_path=detail['poster_path'],
                                        backdrop_path=detail['backdrop_path'],
                                        popularity=detail['popularity'],
                                        vote_count=detail['vote_count'],
                                        vote_average=detail['vote_average'],
                                        adult=detail['adult'],
                                        original_language=detail['original_language'],
                                        runtime=detail['runtime'],
                                        status=detail['status'],
                                        tagline=detail['tagline'],
                                        budget=detail['budget'],
                                        revenue=detail['revenue'],
                                        homepage=detail['homepage'],
                                        now_playing=True,
                                        )
            for res in detail['genres']:
                if not Genre.objects.filter(g_id=res['id']).exists():
                    genre = Genre.objects.create(g_id=res['id'],
                                                name=res['name'])
                else:
                    genre = Genre.objects.get(g_id=res['id'])
                MovieGenre.objects.create(movie=movie,
                                          genre=genre)
            
            for res in keywords['keywords']:
                if not Keyword.objects.filter(k_id=res['id']).exists():
                    keyword = Keyword.objects.create(k_id=res['id'],
                                                    name=res['name'])
                else:
                    keyword = Keyword.objects.get(k_id=res['id'])
                MovieKeyword.objects.create(movie=movie,
                                            keyword=keyword)
        else:
            movie = Movie.objects.get(m_id=response['id'])
            movie.now_playing = True
            movie.save()
        
    now_playings = Movie.objects.filter(now_playing=True)
    serializer = MovieListSerializer(now_playings, many=True)
    return Response(serializer.data)

# def edit_data(request):
#     params = {
#                 'api_key' : '1c495200bf8a0c1956a9c60b7877da9c',
#                 'language' : 'en-US',
#             }
    
#     movies = get_list_or_404(Movie)
    
#     for movie in movies:
#         path = f'/movie/{movie.m_id}'
#         response = requests.get(BASE_URL+path, params=params).json()

#         movie.poster_path = response.get('poster_path', '')
#         movie.backdrop_path = response.get('backdrop_path', '')
#         movie.adult = response.get('adult', '')
#         movie.overview = response.get('overview', '')
#         movie.title = response.get('title', '')
#         movie.tagline = response.get('tagline', '')
#         movie.save()
    
    
# def load_genre(request):
#     path_genre = '/genre/movie/list'
#     params = {
#         'api_key' : '1c495200bf8a0c1956a9c60b7877da9c',
#         'language' : 'ko-KR',
#         'region': 'KR'
#     }
#     response_genre = requests.get(BASE_URL+path_genre, params=params).json()['genres']
#     for res in response_genre:
#         if not Genre.objects.filter(name=res['name']).exists():
#             Genre.objects.create(g_id=res['id'],
#                                 name=res['name'])
    

# @api_view(['GET'])
# def test(request):
    
#     movie_json = open('C:/Users/82102/Desktop/fresh-tomatoes/django/movies/data/tmdb.json', encoding='UTF8')
#     movie_list = json.load(movie_json)
#     #print(movie_list[0], movie_list[1])
#     for movie in movie_list:
#         one_movie = Movie.objects.create(m_id=movie['id'],
#                             title=movie['title'],
#                             overview=movie['overview'],
#                             release_date=movie['release_date'],
#                             popularity=movie['popularity'],
#                             vote_count=movie['vote_count'],
#                             vote_average=movie['vote_average'],
#                             original_language=movie['original_language'],
#                             runtime=movie['runtime'],
#                             status=movie['status'],
#                             tagline=movie['tagline'],
#                             budget=movie['budget'],
#                             revenue=movie['revenue'],
#                             homepage=movie['homepage']
#                             )
#         print(one_movie)
#         #print(movie['genres'])
#         for element in movie['genres']:
#             if not Genre.objects.filter(g_id=element['id']).exists():
#                 Genre.objects.create(g_id=element['id'],
#                                      name=element['name'])
#             genre = Genre.objects.get(g_id=element['id'])
#             MovieGenre.objects.create(movie=one_movie,
#                                      genre=genre)
#         for element in movie['keywords']:
#             if not Keyword.objects.filter(k_id=element['id']).exists():
#                 Keyword.objects.create(k_id=element['id'],
#                                        name=element['name'])
#             keyword = Keyword.objects.get(k_id=element['id'])
#             MovieKeyword.objects.create(movie=one_movie,
#                                         keyword=keyword)
    # movies = Movie.objects.all()
    # serializer = MovieListSerializer(movies, many=True)
    # return Response(serializer.data)