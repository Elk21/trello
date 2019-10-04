import json
# from config import *
from src.config import OMDB_TOKEN
import requests
from src.wiki import get_wiki_film_name


def find_omdb(film, t='series'):
    '''
        Find film/series or episodes by its name via OMDb api
        Returns dict containing title, year, raiting and plot
    '''

    url = f'http://www.omdbapi.com/?apikey={OMDB_TOKEN}&s={film}&type={t}'
    response = json.loads(json.dumps(requests.get(url).json()))

    if response['Response'] == 'False':
        print('----- Cant find film -----')
        return None

    search = response['Search'][0]
    film_id = search['imdbID']

    url = f'http://www.omdbapi.com/?apikey={OMDB_TOKEN}&i={film_id}'
    film = requests.get(url).json()

    info = {}

    info['title'] = film['Title']
    try:
        info['year'] = film['Year']
    except Exception as e:
        print(e)
        info['year'] = ''

    try:
        info['imdb'] = film['imdbRating']
    except Exception as e:
        print(e)
        info['imdb'] = ''

    try:
        info['plot'] = film['Plot']
    except Exception as e:
        print(e)
        info['plot'] = ''

    try:
        info['genres'] = film['Genre']
    except Exception as e:
        print(e)
        info['Genre'] = ''

    return info


def find_film(film):
    '''
        Find film by its correct name
        Returns dict containing title, year, raiting and plot
    '''
    film = get_wiki_film_name(film)
    return find_omdb(film, 'movie')


def find_series(series):
    '''
        Find series by its correct name
        Returns dict containing title, year, raiting and plot
    '''

    return find_omdb(series, 'series')
