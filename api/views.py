import datetime

from rest_framework import viewsets, filters

from movies.models import Movie, Time, Genre, Country
from .permissions import ReadOnly
from .serializers import MovieSerializer, GenreSerializer, TimeSerializer

PATH_SOON = '/api/v1/getMoviesSoon/'


class MovieViewSet(viewsets.ModelViewSet):
    permission_classes = (ReadOnly,)
    serializer_class = MovieSerializer

    def get_queryset(self):
        now = datetime.datetime.now().date()
        if self.request.path == PATH_SOON:
            queryset = Movie.objects.filter(start_date__gt=now)
            return queryset
        queryset = Movie.objects.filter(start_date__lte=now).filter(end_date__gt=now)
        return queryset


class MoviesByDirectorViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    permission_classes = (ReadOnly,)
    serializer_class = MovieSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('director',)


class MoviesByGenreViewSet(viewsets.ModelViewSet):
    permission_classes = (ReadOnly,)
    serializer_class = MovieSerializer

    def get_queryset(self):
        searched_genre = self.request.query_params['search']
        queryset = Movie.objects.filter(genres__name=searched_genre)
        return queryset


class MoviesByTimeViewSet(viewsets.ModelViewSet):
    permission_classes = (ReadOnly,)
    serializer_class = MovieSerializer

    def get_queryset(self):
        searched_time = self.request.query_params['search'] + ':00:00'
        time_gap = str(int(self.request.query_params['search']) + 1) + ':00:00'
        queryset = Movie.objects.filter(
            start_time__time__gte=searched_time).filter(
            start_time__time__lt=time_gap)
        return queryset


class AllGenresViesSet(viewsets.ModelViewSet):
    permission_classes = (ReadOnly,)
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class AllTimeViewSet(viewsets.ModelViewSet):
    permission_classes = (ReadOnly,)
    queryset = Time.objects.all()
    serializer_class = TimeSerializer
