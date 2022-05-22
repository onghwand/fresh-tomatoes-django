import requests
from django.shortcuts import get_list_or_404, get_object_or_404
from yaml import serialize


from .serializers.movie import MovieListSerializer, MovieSerializer
from .serializers.review import ReviewSerializer
from .models import Movie, MovieGenre, Genre, Review
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
    pass

@api_view(['GET']) 
def now_playing(request):
    pass

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
def movie_list(request, mode):
    if mode == 'now_playing':
        path_now_playing = '/movie/now_playing'
        # path_genre = '/genre/movie/list'
        params = {
            'api_key' : '1c495200bf8a0c1956a9c60b7877da9c',
            'language' : 'en-US',
            'region': 'US'
        }
        # response_genre = requests.get(BASE_URL+path_genre, params=params).json()['genres']
        # for res in response_genre:
        #     if not Genre.objects.filter(name=res['name']).exists():
        #         Genre.objects.create(g_id=res['id'],
        #                             name=res['name'])
        
        response_now_playing = requests.get(BASE_URL+path_now_playing, params=params).json()['results']
        for res in response_now_playing:
            if not Movie.objects.filter(title=res['title']).exists():
                movie = Movie.objects.create(m_id=res['id'],
                                    title=res['title'],
                                    overview=res['overview'],
                                    release_date=res['release_date'],
                                    poster_path=res['poster_path'],
                                    backdrop_path=res['backdrop_path'],
                                    popularity=res['popularity'],
                                    vote_count=res['vote_count'],
                                    vote_average=res['vote_average'],
                                    adult=res['adult']
                                    #original_language=res_detail['original_language'],
                                    #runtime=res_detail['runtime'],
                                    #status=res_detail['status'],
                                    #tagline=res_detail['tagline']
                                    )
                for genre_id in res['genre_ids']:
                    genre = Genre.objects.get(g_id=genre_id)
                    MovieGenre.objects.create(movie=movie,
                                            genre=genre)
                    
                # path_detail = f"movie/{movie.m_id}"
                # res_detail = requests.get(BASE_URL+path_detail, params=params)
                # print(res_detail)
                # print(res['title'],res_detail['original_language'],res_detail['runtime'],res_detail['status'],res_detail['tagline']) 
            
        movies = Movie.objects.all()
        serializer = MovieListSerializer(movies, many=True)
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