from rest_framework import generics
from .models import Movie
from .serializers import MovieSerializer


class MovieListAPI(generics.ListAPIView):
    queryset = Movie.objects.all().order_by('release_date')
    serializer_class = MovieSerializer


class MovieDetailAPI(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
