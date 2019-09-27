import json
import requests
from bs4 import BeautifulSoup


'''
    TODO:
        1. Add webhooks
        2. Add labels with raiting for cards
        3. Parse books
        4. Parse genres for games via metacritic
        5. Set game's card name after finding a correct game
        5. Set game's card name after finding a correct game
'''


YOUTUBE_TOKEN = 'AIzaSyBplMZXvkzWctymn5L-1Jh6T3IG5wp0e5k'
OMDB_TOKEN = '2f27933'
TRELLO_KEY = 'a2c44f7078a2585af30d658cef7287a3'
TRELLO_TOKEN = '25f4b79910f15728b2c19ecc4aa86aebbd0c0ae3d0e66d1ce5bdfa6c5a9a530a'

BOARD_ID = 'WIopiWu2'
GAMES_LIST_ID = '5d70d52b4cf76d5afd305e7c'
FILMS_LIST_ID = '5d70c3692f0fe53b6fa1858f'
BOOKS_LIST_ID = '5d70c3713b458e052e970007'
SERIES_LIST_ID = '5d70c36e3d2b91774428831f'

URL = f'https://api.trello.com/1/boards/{BOARD_ID}/cards&key={TRELLO_KEY}&token={TRELLO_TOKEN}'
WIKI_URL = "https://en.wikipedia.org/w/api.php"


def get_metacritic_score(name, platform='pc'):
    '''
        Scrape metacritic for user score and critic score
        Returns dict:
            {
                'user score': <user score>,
                'user count': <user count>,
                'critic score': <critic score>,
                'critic count': <critic count>
            }
    '''

    name = name.replace(' ', '-').lower()
    url = f'https://www.metacritic.com/game/{platform}/{name}'
    hdr = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=hdr)
        soup = BeautifulSoup(response.text, 'html.parser')

        critic_raiting = soup.find("span", itemprop="ratingValue").text

        user_raiting = soup.find_all(
            "div", class_='userscore_wrap feature_userscore')
        user_raiting = user_raiting[0].find('div', class_='metascore_w').text

        summary = soup.find_all('div', class_='summary')

        critic_count = summary[0].find('span', class_='').text.strip()

        user_count = summary[1].find('a').text.strip().split()[0]

        result = {
            'user score': user_raiting,
            'user count': user_count,
            'critic score': critic_raiting,
            'critic count': critic_count
        }

        return result
    except Exception:
        print('Cant find game on metacritic')
        return None


def write_out(data):
    with open('out.json', 'w') as out:
        out.write(data)


def get_lists():
    '''
        Returns json of lists from spesific board
    '''

    url = f"https://api.trello.com/1/boards/{BOARD_ID}/lists"
    querystring = {
        "cards": "none",
        "card_fields": "all",
        "key": f"{TRELLO_KEY}",
        "token": f"{TRELLO_TOKEN}"}

    response = requests.request("GET", url, params=querystring)
    return json.loads(json.dumps(response.json()))


def get_cards(list_id):
    '''
        Returns json of cards from specific list
    '''

    url = f"https://api.trello.com/1/lists/{list_id}/cards"
    querystring = {
        'members': 'false',
        "key": f"{TRELLO_KEY}",
        "token": f"{TRELLO_TOKEN}"}

    response = requests.request("GET", url, params=querystring)
    return json.loads(json.dumps(response.json()))


def put_desc(card_id, desc):
    '''
        Put description to a card
    '''

    url = f"https://api.trello.com/1/cards/{card_id}/"
    querystring = {
        "desc": f"{desc}",
        "key": f"{TRELLO_KEY}",
        "token": f"{TRELLO_TOKEN}"}

    response = requests.request("PUT", url, params=querystring)
    return json.loads(json.dumps(response.json()))


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
    film = json.loads(json.dumps(requests.get(url).json()))

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


def get_trailer(text):
    '''
        Search YouTube for < film name > trailer and return top 2 results
        Returns array of dicts with title, link and thumbnails image
    '''

    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=2&q={text} trailer&key={YOUTUBE_TOKEN}'

    vids = requests.get(url).json()
    videos = []
    for video in vids['items']:
        result = {}
        result['title'] = video['snippet']['title']
        result['link'] = 'https://www.youtube.com/watch?v=' + \
            video['id']['videoId']
        result['img'] = video['snippet']['thumbnails']['high']['url']
        videos.append(result)

    return videos


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


def add_checklist(card_id, name='Select game'):
    '''
        Add checklist for card
        Returns id of created checklist
    '''

    url = "https://api.trello.com/1/checklists"
    querystring = {"idCard": card_id, "name": name,
                   "key": TRELLO_KEY, "token": TRELLO_TOKEN}
    response = requests.request("POST", url, params=querystring)
    checklist_id = response.json()['id']

    return checklist_id


def add_checklist_item(checklist_id, name, pos='bottom', checked='false'):
    '''
        Add item for a checklist
        Returns id of created checklist
    '''

    url = f"https://api.trello.com/1/checklists/{checklist_id}/checkItems"
    querystring = {"name": name, "pos": pos, "checked": checked,
                   "key": TRELLO_KEY, "token": TRELLO_TOKEN}
    response = requests.request("POST", url, params=querystring)

    return response.json()['idChecklist']


def get_checklists_id(card_id):
    url = f"https://api.trello.com/1/cards/{card_id}/checklists"
    querystring = {"checkItems": "all", "checkItem_fields": "name,nameData,pos,state",
                   "filter": "all", "fields": "all", "key": TRELLO_KEY,
                   "token": TRELLO_TOKEN}
    response = requests.request("GET", url, params=querystring)

    ar = []
    for x in response.json():
        ar.append(x['id'])

    return ar


def get_checklist_items(checklist_id):
    '''
        Get all ckecklist items from checklist
        Returns json with data for each item
    '''

    url = f"https://api.trello.com/1/checklists/{checklist_id}/checkItems"
    querystring = {"fields": "all",
                   "key": TRELLO_KEY, "token": TRELLO_TOKEN}
    response = requests.request("GET", url, params=querystring)

    return response.json()


def check_if_game_selected(checklist_id):
    '''
        Check if any item in games checklist is selected
        If so return the first one selected
        Otherwise return False
    '''

    items = get_checklist_items(checklist_id)
    for item in items:
        if item['state'] == 'complete':
            return item['name']
    return False


def delete_all_checklists(card_id):
    '''
        Delete all checklists from card by given card id
    '''

    querystring = {"key": TRELLO_KEY, "token": TRELLO_TOKEN}
    ids = get_checklists_id(card_id)

    for id in ids:
        url = f"https://api.trello.com/1/cards/{card_id}/checklists/{id}"
        response = requests.request("DELETE", url, params=querystring)


def create_games_selector(card_id, card_name, games):
    '''
        Create checklist for a card and fill it
        with wiki search results of card name as items
    '''

    delete_all_checklists(card_id)
    checklist_id = add_checklist(card_id)
    for game in games:
        text = f'**{game[0]}** - {game[1]}'
        add_checklist_item(checklist_id, text)


def create_game_desc(game_name, game_desc):
    print(game_name)
    scores = get_metacritic_score(game_name)

    if not scores:
        return None

    user_score = scores['user score']
    user_count = scores['user count']
    critic_score = scores['critic score']
    critic_count = scores['critic score']

    s = f'# {game_name}  \n{game_desc}  \n***  \nCritic score: **{critic_score}**  Critic count: {critic_count}  \n User score: **{user_score}**  User count: {user_count} '

    return s


def fill_games():
    cards = get_cards(GAMES_LIST_ID)
    for card in cards:
        card_name = card['name']
        card_id = card['id']
        print(f'***** {card_name} {card_id} *****\n')

        card_desc = card['desc']
        if card_desc != '':
            continue

        checklist = get_checklists_id(card_id)
        if len(checklist) > 0:
            selected_game = check_if_game_selected(checklist[0])
            if selected_game:
                game_name = selected_game.split('** - ')[0].replace('**', '')
                game_desc = selected_game.split('** - ')[1]

                delete_all_checklists(card_id)

                desc = create_game_desc(game_name, game_desc)
                if desc:
                    put_desc(card_id, desc)
            continue

        games = get_games_name(card_name)
        if len(games) == 1:
            game_name = games[0][0]
            game_desc = games[0][1]

            desc = create_game_desc(game_name, game_desc)
            if desc:
                put_desc(card_id, desc)
            continue

        create_games_selector(card_id, card_name, games)


def fill_list(list_id, t):
    cards = get_cards(list_id)

    for card in cards:
        card_name = card['name']
        card_id = card['id']
        print(card_name, card_id)

        film = find_omdb(card_name, t)
        if not film:
            put_desc(card_id, '# Can not find film with this title')
        else:
            film_title = film['title']
            film_year = film['year']
            film_raiting = film['imdb']
            film_plot = film['plot']

            trailers = get_trailer(film_title)
            trailer1_title = trailers[0]['title']
            trailer1_link = trailers[0]['link']
            trailer1_img = trailers[0]['img']
            trailer2_title = trailers[1]['title']
            trailer2_link = trailers[1]['link']
            trailer2_img = trailers[1]['img']

            desc = f'# **{film_title}**  \n---  \n### Year: {film_year}  \n### IMDb raiting: **{film_raiting}**  \n---  \n{film_plot}  \n  \n---  \n### *{trailer1_title}*  \n[![TRAILER 1]({trailer1_img})]({trailer1_link})  \n---  \n### *{trailer2_title}*  \n[![TRAILER 1]({trailer2_img})]({trailer2_link})'
            put_desc(card_id, desc)


if __name__ == '__main__':
    # fill_list(SERIES_LIST_ID, 'series')
    # fill_list(FILMS_LIST_ID, 'movie')
    # fill_games()
    # delete_checklist('5d84bd4bfea44b3297716352')
    # id = add_checklist('5d84bd4bfea44b3297716352')
    # add_checklist_item(id, 'shit')
    # print(get_lists())
    # delete_all_checklists('5d84bd4bfea44b3297716352')
    fill_games()
