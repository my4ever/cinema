import requests

URL = ' https://db9c-195-78-104-62.ngrok.io/api/v1/'



def get_movies_now():
    command = 'getMoviesNow/'
    movies = requests.get(URL + command)
    return movies

def get_movies_soon():
    command = 'getMoviesSoon/'
    movies = requests.get(URL + command)
    return movies

REQUEST = {
    '/now': get_movies_now(),
    '/soon': get_movies_soon(),
}