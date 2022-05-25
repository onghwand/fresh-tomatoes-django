from django.urls import path
from . import views

urlpatterns = [
    # movies
    # path('load_genre/', views.load_genre), 장르 받아왔던 함수
    # path('get_movies/', views.test), csv -> json -> dbsqlite3로 데이터 옮겼던 함수
    # path('edit_data/', views.edit_data), 부족한 poster_path, adult, backdrop_path 받아오는데 쓴 함수
    #path('movie_list/<str:mode>/', views.movie_list), # 영화 종류별 리스트 반환 total, latest, now_playing, popular, top_rated, upcoming
    
    path('', views.movie),
    path('<int:movie_pk>/', views.movie_detail), # 개별 영화 detail 정보
    path('<int:movie_pk>/like/', views.like_movie), # 영화 좋아요
    path('<int:movie_pk>/related/genre/', views.related_genre), # 관련된 영화 정보 - 같은 장르 
    path('<int:movie_pk>/related/release_date/', views.related_release_date), # 관련된 영화 정보 -비슷한시기
    #path('now_playing/', views.now_playing), # 현재 상영중인 영화 정보
    path('search/', views.search),
    
    # comments
    path('<int:movie_pk>/reviews/', views.review_read_or_create),
    path('<int:movie_pk>/reviews/<int:review_pk>/', views.review_update_or_delete),
    path('<int:movie_pk>/reviews/<int:review_pk>/like/', views.like_review),
    
    #recommendation
    path('recommendation/<mode>/', views.recommendation),
    
    path('<mode>/', views.get_movies), # popular / now_playing / upcoming
]
