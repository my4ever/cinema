from django.urls import path, include
from rest_framework import routers

from . import views

router_v1 = routers.DefaultRouter()
router_v1.register(r'getMovies(Now|Soon)', views.MovieViewSet, basename='movies')
router_v1.register('getMoviesByDirector',
                   views.MoviesByDirectorViewSet, basename='get_director')
router_v1.register('getMoviesByGenre', views.MoviesByGenreViewSet, basename='get_genre')
router_v1.register('getMoviesByTime', views.MoviesByTimeViewSet, basename='get_time')
router_v1.register('getAllGenres', views.AllGenresViesSet, basename='genres')
router_v1.register('getAllTime', views.AllTimeViewSet, basename='time')

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
