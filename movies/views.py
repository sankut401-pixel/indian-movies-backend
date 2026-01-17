from django.views.decorators.csrf import csrf_exempt
from collections import OrderedDict
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework import generics

from .models import Movie
from .models import RatingPrediction
from .serializers import MovieSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ml.predict import predict_rating
from ml.embeddings import get_recommendations_for_movie

# ===========================
# 🌐 WEB VIEWS (HTML)
# ===========================

def home(request):
    query = request.GET.get('q', '')
    release_type = request.GET.get('type', '')
    language = request.GET.get('lang', '')

    movies = Movie.objects.all().order_by('release_date')

    if query:
        movies = movies.filter(title__icontains=query)

    if release_type:
        movies = movies.filter(release_type=release_type)

    if language:
        movies = movies.filter(languages__icontains=language)

    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    grouped_movies = OrderedDict()
    for movie in page_obj:
        grouped_movies.setdefault(movie.release_date, []).append(movie)

    return render(request, 'home.html', {
        'grouped_movies': grouped_movies,
        'page_obj': page_obj,
        'query': query,
        'release_type': release_type,
        'language': language
    })


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movie_detail.html', {'movie': movie})

@csrf_exempt
@api_view(["POST"])
def predict_movie_rating(request):
    synopsis = request.data.get("synopsis", "")
    predicted = predict_rating(synopsis)

    RatingPrediction.objects.create(
        synopsis_text=synopsis,
        predicted_rating=predicted
    )

    return Response({
        "predicted_rating": predicted
    })

def health_check(request):
    return JsonResponse({"status": "ok"})

# ===========================
# 📡 API VIEWS (JSON)
# ===========================

class MovieListAPIView(generics.ListAPIView):
    queryset = Movie.objects.all().order_by('release_date')
    serializer_class = MovieSerializer


@api_view(["GET"])
def recommend_movies(request, movie_id):
    data = get_recommendations_for_movie(movie_id)

    if data is None:
        return Response(
            {"error": "Movie not found"},
            status=404
        )

    return Response(data)
