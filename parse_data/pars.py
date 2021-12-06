import requests
import django
import os
import datetime

from googleapiclient.discovery import build
from bs4 import BeautifulSoup as bs

# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema.settings')  # this should be done first.

# Import settings
django.setup()  # This needs to be done after you set the environ

from movies.models import Country, Room, Genre, Time, Movie
from cinema.settings import GOOGLE_API_AUTH, CINEMA


def parser() -> list:
    """
    Parsing movies from kino-kus.com
    returns list of parsed movies
    """
    # source to get data
    url = CINEMA
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    response = requests.get(url, headers=headers).content
    # raw data
    soup = bs(response, 'html.parser')
    # getting movie blocks
    movies_items = soup.findAll('div', class_='film_block')
    movies = []
    # getting movies info out of raw data
    if movies_items:
        for movie in movies_items:
            movies.append({
                'title': ' '.join(movie.find('p', class_='film_title').get_text(strip=True).split()[0:-1]),
                'country': str(movie.find('p', class_='film_description')).split('<br/>')[0].split('>')[
                    1].strip().split(','),
                'year': int(str(movie.find('p', class_='film_description')).split('<br/>')[1]),
                'director': ', '.join(name for name in str(movie.find('p', class_='film_description')).split(
                    'Режиссёр:')[1].split('<br/>')[0].split('\n')[0].strip().split(',')),
                'actors': ', '.join([name.strip() for name in
                                    movie.find('p', class_='film_description').get_text(strip=True).split('ролях:')[
                               1].split('Зал:')[0].split('-') if name != '']),
                'genres': str(movie.find('p', class_='film_description')).split('<br/>')[2].split('\t')[
                    -1].strip().split(', '),
                'room': str(movie.find('p', class_='film_description')).split('<br/>')[-4].split('Зал:')[1].strip(),
                'start_time': str(movie.find('p', class_='film_description')).split('<br/>')[-3].split('span>')[
                    1].split('<')[0].split(','),
                'start_date': movie.find('p', class_='sessions_and_price').get_text().split('Показ:')[
                    -1].strip().split('\n')[0].split(' — ')[0],
                'end_date': movie.find('p', class_='sessions_and_price').get_text().split('Показ:')[
                    -1].strip().split('\n')[0].split(' — ')[1],

                'price': int(movie.find('p', class_='sessions_and_price').get_text().split('Цена:')[
                    -1].split('р')[0].strip()),
            })
        for m in movies:
            m['trailer'] = 'https://www.youtube.com/watch?v=fNFzfwLM72c&ab_channel=BeeGeesVEVO'
            m['country'] = refactor_country(m['country'])
            m['room'] = refactor_room(m['room'])
            m['genres'] = refactor_genres(m['genres'])
            m['start_time'] = refactor_time(m['start_time'])
            m['start_date'] = refactor_date(m['start_date'])
            m['end_date'] = refactor_date(m['end_date'])
            # m['trailer'] = get_trailer(m['title'])

        return movies


def get_trailer(name: str) -> str:
    """
    Getting a trailer via YouTube APIs
    for the movie.
    """
    youtube = build('youtube', 'v3', developerKey=GOOGLE_API_AUTH)
    request = youtube.search().list(
        part='snippet',
        type='video',
        q=name + ' трейлер',
        regionCode='RU',
        maxResults=1
    )
    trailer = request.execute()
    return f"https://www.youtube.com/watch?v={trailer['items'][0]['id']['videoId']}"


def refactor_country(country: list) -> list:
    """Refactoring country into instance of Country model."""
    refactored_county = []
    for c in country:
        country_instance, status = Country.objects.get_or_create(name=c.strip())
        refactored_county.append(country_instance)
    return refactored_county


def refactor_room(room: str):
    """Refactoring room into instance of Room model."""
    room_instance, status = Room.objects.get_or_create(name=room)
    return room_instance


def refactor_genres(genres: list) -> list:
    """Refactoring genre into instance of Genre model."""
    refactored_genres = []
    for genre in genres:
        genre_instance, status = Genre.objects.get_or_create(name=genre)
        refactored_genres.append(genre_instance)
    return refactored_genres


def refactor_time(time: list) -> list:
    """Refactoring time into instance of Time model."""
    refactored_time = []
    for t in time:
        refactored_time.append(Time.objects.get_or_create(time=datetime.time(hour=int(t[0:2]), minute=int(t[-2:])))[0])
    return refactored_time


def refactor_date(date: str):
    """Refactoring date into instance of DateField."""
    return datetime.date(year=int(date[-4:]), month=int(date[-7:-5]), day=int(date[:2]))


def adding_movies_into_db():
    """
    Adding movies into DB.
    """
    movies = parser()
    for m in movies:
        movie = Movie.objects.create(
            title=m['title'],
            year=m['year'],
            director=m['director'],
            actors=m['actors'],
            trailer=m['trailer'],
            room=m['room'],
            start_date=m['start_date'],
            end_date=m['end_date'],
            price=m['price']
            )

        for country in m['country']:
            movie.country.add(country)

        for genre in m['genres']:
            movie.genres.add(genre)

        for start_time in m['start_time']:
            movie.start_time.add(start_time)


if __name__ == '__main__':
    print(parser())
    adding_movies_into_db()
