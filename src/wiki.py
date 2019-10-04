import requests

WIKI_URL = "https://en.wikipedia.org/w/api.php"


def get_wiki_film_name(name):
    '''
        Search wiki for correct film name
        if search result contains '(film)' return in
        in other case return first search result
        Returns film name
    '''
    session = requests.Session()

    PARAMS = {
        "action": "opensearch",
        "namespace": "0",
        "search": name,
        "limit": "5",
        "format": "json"
    }

    response = session.get(url=WIKI_URL, params=PARAMS)
    data = response.json()
    film_name = data[1][0]

    for film in data[1]:
        if 'film' in film:
            film_name = film.replace(' (film)', '')
            film_name = film_name.split('(')[0].strip()
            break
    return film_name


def get_games_name(name):
    '''
        Search wiki for pages with < name > in title
        and 'video game' in page description
        Return list of lists [ < game name > , < wiki page description > ]
    '''
    S = requests.Session()

    PARAMS = {
        "action": "opensearch",
        "namespace": "0",
        "search": name,
        "limit": "5",
        "format": "json"
    }

    R = S.get(url=WIKI_URL, params=PARAMS)
    DATA = R.json()

    ar = []
    for i, x in enumerate(DATA[1]):
        if 'video game' in x or 'game' in DATA[2][i]:
            ar.append([x, DATA[2][i]])
    return ar


def get_film_names(name):
    '''
        Search wiki for pages with < name > in title
        and 'video game' in page description
        Return list of lists [ < game name > , < wiki page description > ]
    '''
    S = requests.Session()

    PARAMS = {
        "action": "opensearch",
        "namespace": "0",
        "search": name,
        "limit": "5",
        "format": "json"
    }

    R = S.get(url=WIKI_URL, params=PARAMS)
    DATA = R.json()

    ar = []
    for i, x in enumerate(DATA[1]):
        # if 'film' in x or 'film' in DATA[2][i]:
        y = x.split('(')[0].strip()
        ar.append([y, DATA[2][i]])
    return ar
