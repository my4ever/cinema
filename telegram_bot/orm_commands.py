import datetime

from movies.models import Movie

start_message = (
    """Здаравствуйте. Я - Помощник кинотеарта Русь. Могу показать вам список фильмов которые идут в прокате сегодня:
    сегодня в кино - нажмите.
Или показать вам фильмы которые скоро будут в прокате:
    скоро в кино - нажмите.""")


def get_now():
    return datetime.datetime.now().date()


def get_movies_now():
    now = get_now()
    movies = Movie.objects.filter(start_date__lte=now).filter(end_date__gt=now)
    return movies


def get_movies_soon():
    now = get_now()
    movies = Movie.objects.filter(start_date__gte=now)
    return movies


def get_genres():
    now = get_now()
    movies = Movie.objects.filter(start_date__lte=now).filter(end_date__gt=now)
    genres_query = set([movie.genres.all() for movie in movies])
    genres = []
    for genre in genres_query:
        for g in genre:
            genres.append(g.name)
    return sorted(set(genres))


def get_movies_by_genre(genre):
    now = get_now()
    movies = Movie.objects.filter(genres__name=genre).filter(start_date__lte=now).filter(end_date__gt=now)
    return movies


def get_start_time():
    now = get_now()
    movies = Movie.objects.filter(start_date__lte=now).filter(end_date__gt=now)
    starts = set([movie.start_time.all() for movie in movies])
    movie_starts = []
    for start in starts:
        for time in start:
            movie_starts.append(time.time)
    return _sorted_time(set(movie_starts))


def _sorted_time(times):
    sorted_time = []
    for time in sorted(times):
        sorted_time.append(str(time)[:-6])
    return sorted_time


def get_movies_by_time(time):
    now = get_now()
    searched_time = time + ':00:00'
    time_gap = str(int(time) + 1) + ':00:00'
    movies = Movie.objects.filter(
            start_time__time__range=(searched_time, time_gap)).filter(
        start_date__lte=now).filter(end_date__gt=now)
    for m in movies:
        print(m.title)
    return movies


REQUEST = {
    'сегодня в кино': get_movies_now,
    'скоро в кино': get_movies_soon,
}
