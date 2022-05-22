import json
from .models import Keyword, Movie, MovieGenre, MovieKeyword, Genre

movie_json = open('django/movies/data/tmdb.json', encoding='UTF8')
movie_list = json.load(movie_json)
#print(movie_list[0])

for movie in movie_list:
    movie = Movie.objects.create(m_id=movie['id'],
                         title=movie['title'],
                         overview=movie['overview'],
                         release_date=movie['release_date'],
                         popularity=movie['popularity'],
                         vote_count=movie['vote_count'],
                         vote_average=movie['vote_average'],
                         original_language=movie['original_language'],
                         runtime=movie['runtime'],
                         status=movie['status'],
                         tagline=movie['tagline'],
                         budget=movie['budget'],
                         revenue=movie['revenue'],
                         homepage=movie['homepage']
                         )
    for element in movie['genres']:
        genre = Genre.objects.get(g_id=element['id'])
        MovieGenre.objects.create(movie=movie,
                                  genre=genre)
    for element in movie['keyword']:
        if not Keyword.objects.filter(k_id=element['id']).exists():
            Keyword.objects.create(k_id=element['id'],
                                   name=element['name'])
        keyword = Keyword.objects.get(k_id=element['id'])
        MovieKeyword.objects.create(movie=movie,
                                    keyword=keyword)
        