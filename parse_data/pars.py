import requests
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from bs4 import BeautifulSoup as bs

from movies.models import Country

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
                'country': str(movie.find('p', class_='film_description')).split('<br/>')[0].split('>')[1].strip().split(','),
                'year': str(movie.find('p', class_='film_description')).split('<br/>')[1],
                'director': str(movie.find('p', class_='film_description')).split('Режиссёр:')[1].split('<br/>')[0].split('\n')[0].strip().split(','),
                'actors': [name.strip() for name in
                           movie.find('p', class_='film_description').get_text(strip=True).split('ролях:')[1].split('Зал:')[0].split('-') if name != ''],
                'genres': str(movie.find('p', class_='film_description')).split('<br/>')[2].split('\t')[-1].strip().split(', '),
                'room': str(movie.find('p', class_='film_description')).split('<br/>')[-4].split('Зал:')[1].strip(),
                'start_time': str(movie.find('p', class_='film_description')).split('<br/>')[-3].split('span>')[1].split('<')[0].split(','),
                'start_date': movie.find('p', class_='sessions_and_price').get_text().split('Показ:')[-1].strip().split('\n')[0].split(' — ')[0],
                'end_data': movie.find('p', class_='sessions_and_price').get_text().split('Показ:')[-1].strip().split('\n')[0].split(' — ')[1],

                'price': movie.find('p', class_='sessions_and_price').get_text().split('Цена:')[-1].split('р')[0].strip(),
            })
        for m in movies:
            # m['country'] = refactor_country(m['country'])
            m['trailer'] = 'https://www.youtube.com/watch?v=fNFzfwLM72c&ab_channel=BeeGeesVEVO'
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


# def refactor_country(country: list): # TODO: find out what causes the problem
#     refactored_county = []
#     for c in country:
#         pass
#         refactored_county.append(Country.objects.get_or_create(c))
#
#     print(refactored_county)
#     return refactored_county

parser()


