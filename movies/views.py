from collections import OrderedDict
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from rest_framework import generics

from .models import Movie
from .serializers import MovieSerializer


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


# ===========================
# 📡 API VIEWS (JSON)
# ===========================

class MovieListAPIView(generics.ListAPIView):
    queryset = Movie.objects.all().order_by('release_date')
    serializer_class = MovieSerializer
