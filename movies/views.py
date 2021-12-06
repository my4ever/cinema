import datetime

from django.views.generic import ListView

from .models import Movie


class MovieList(ListView):
    """
    Returns list of movies witch are playing this week or movies
    that going to be soon.
    Optional can delete all movies that play date has expired.
    """
    template_name = 'movies/index.html'
    context_object_name = 'movies'

    def get_queryset(self):
        now = datetime.datetime.now().date()
        if self.request.path == '/soon/':
            queryset = Movie.objects.filter(start_date__gt=now)
            return queryset
        # all_movies = Movie.objects.all()
        # for movie in all_movies:  # Delete all movies in witch play time has expired
        #     if movie.end_date <= now:
        #         movie.delete()
        queryset = Movie.objects.filter(start_date__lte=now).filter(end_date__gt=now)
        return queryset


