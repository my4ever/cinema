import json

from datetime import datetime as dt
from django.shortcuts import HttpResponse

from . import orm_commands
from .create import Bot
from cinema.settings import BOT_TOKEN, ADMIN_TELEGRAM_ID

data_movies_update = None
bot = Bot(BOT_TOKEN)


def telegram_data(request):
    json_msg = json.load(request)
    message = json_msg['message']['text']
    chat_id = json_msg['message']['chat']['id']
    user_id = json_msg['message']['from']['id']
    # first_name = json_msg['message']['from']['first_name']
    # username = json_msg['message']['from']['username']

    # menu = {
    #     '/start': start_message(chat_id),
    #     'сегодня в кино': get_movies(chat_id, message),
    #     'скоро в кино': get_movies(chat_id, message),
    #     'жанры': get_genres(chat_id),
    #     'начало сеансов': get_time(chat_id)
    # }

    if request.method == 'POST':

        if message in orm_commands.get_genres():
            get_movies_by_genre(chat_id, message)

        if message in orm_commands.get_start_time():
            get_movies_by_time(chat_id, message)

        if message == '/start':
            start_message(chat_id)

        if message == 'сегодня в кино':
            get_movies(chat_id, message)

        if message == 'скоро в кино':
            get_movies(chat_id, message)

        if message == 'жанры':
            get_genres(chat_id)

        if message == 'начало сеансов':
            get_time(chat_id)

        print('we got message: ', message, '\n',
              'from: ', 'user_id: ', user_id,
              # 'last_name: ', last_name, '\n',
              # 'first_name: ', first_name, '\n',
              # 'username: ', username, '\n',
              'chat id :', chat_id, '\n')

    return HttpResponse({'name': 'Я - робот!'})


def start_message(chat_id):
    bot.send_message(chat_id, orm_commands.start_message)


def send_movie(chat_id, movies):
    for movie in movies:
        message = (
            'Название: '
            f'{movie.title}\n'
            'Жанр: '
            f'{", ".join(genre.name for genre in movie.genres.all())}\n'
            'Сансы: '
            f'{", ".join([str(start.time)[:-3] for start in movie.start_time.all()])}\n'
            f'Цена: {movie.price} руб.\n'
            f'{movie.trailer}'
        )
        bot.send_message(chat_id, message)


def get_movies(chat_id, message):
    movies = orm_commands.REQUEST[message]()
    if orm_commands.REQUEST[message]():
        send_movie(chat_id, movies)

def get_genres(chat_id):
    genres = orm_commands.get_genres()
    message = '\n'.join(genres)
    keyboard = []
    for genre in genres:
        keyboard.append([{'text': f'{genre}'}],)
    bot.send_message(chat_id=chat_id, text=message, keyboard=keyboard)


def get_movies_by_genre(chat_id, genre):
    movies = orm_commands.get_movies_by_genre(genre)
    send_movie(chat_id, movies)


def get_time(chat_id):
    times = orm_commands.get_start_time()
    message = '\n'.join(times)
    keyboard = []
    for genre in times:
        keyboard.append([{'text': f'{genre}'}],)
    bot.send_message(chat_id=chat_id, text=message, keyboard=keyboard)


def get_movies_by_time(chat_id, time):
    movies = orm_commands.get_movies_by_time(time)
    send_movie(chat_id, movies)
