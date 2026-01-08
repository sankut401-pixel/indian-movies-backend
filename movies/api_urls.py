from django.urls import path
from .api_views import MovieListAPI, MovieDetailAPI

urlpatterns = [
    path('movies/', MovieListAPI.as_view(), name='api_movie_list'),
    path('movies/<int:pk>/', MovieDetailAPI.as_view(), name='api_movie_detail'),
]
