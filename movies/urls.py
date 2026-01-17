from django.urls import path
from .views import (
    MovieListAPIView,
    predict_movie_rating,
    recommend_movies,
    health_check,
)

urlpatterns = [
    # API endpoints
    path("movies/", MovieListAPIView.as_view(), name="movie-list"),
    path("predict-rating/", predict_movie_rating, name="predict-rating"),
    path("recommend/<int:movie_id>/", recommend_movies, name="recommend-movies"),

    # Health check (Render)
    path("healthz/", health_check, name="health-check"),
]
