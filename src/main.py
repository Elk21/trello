import json
import requests
from bs4 import BeautifulSoup
from config import TRELLO_TOKEN, TRELLO_KEY
from imdb import find_film, find_omdb, find_series
from metacritic import get_metacritic_score
from wiki import get_games_name, get_film_names
from youtube import get_trailer
from images import draw_metacritic_image, draw_imdb_rating
from trello import *

'''
    TODO:
        1. Add webhooks
        2. Add labels with raiting for cards
        3. Parse books
        4. Parse genres for games via metacritic
'''


GAMES_LIST_ID = '5d70d52b4cf76d5afd305e7c'
FILMS_LIST_ID = '5d70c3692f0fe53b6fa1858f'
BOOKS_LIST_ID = '5d70c3713b458e052e970007'
SERIES_LIST_ID = '5d70c36e3d2b91774428831f'

URL = f'https://api.trello.com/1/boards/{BOARD_ID}/cards&key={TRELLO_KEY}&token={TRELLO_TOKEN}'


def check_if_item_selected(checklist_id):
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


def create_media_selector(card_id, items):
    '''
        Create checklist for a card and fill it
        with wiki search results of card name as items
    '''

    delete_all_checklists(card_id)
    checklist_id = add_checklist(card_id)
    for item in items:
        text = f'**{item[0]}** - {item[1]}'
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
    genres = ', '.join(scores['genres'])

    s = f'# {game_name}  \n{game_desc}  \n***  \
            \nCritic score: **{critic_score}**  Critic count: {critic_count}  \
            \nUser score: **{user_score}**  User count: {user_count}  \
            \n***  \nGenres: {genres}'

    return s


def fill_game_card(game_name, game_desc, card_id):
    '''
        Fill game description
        Add image with metacritic scores 
        Rename card with the name found on wiki
    '''
    desc = create_game_desc(game_name, game_desc)
    if desc:
        add_desc(card_id, desc)
        add_metacritic_image(game_name, card_id)
    add_card_name(card_id, game_name)


def fill_games():
    cards = get_cards(GAMES_LIST_ID)
    for card in cards:
        card_name = card['name']
        card_id = card['id']
        card_desc = card['desc']
        games = get_games_name(card_name)
        checklist = get_checklists_id(card_id)

        print(f'***** {card_name} {card_id} *****\n')

        if len(games) == 1:
            game_name = games[0][0]
            game_desc = games[0][1]

            fill_game_card(game_name, game_desc, card_id)
            continue

        if len(checklist) > 0:
            selected_game = check_if_item_selected(checklist[0])
            if selected_game:
                game_name = selected_game.split('** - ')[0].replace('**', '')
                game_desc = selected_game.split('** - ')[1]

                delete_all_checklists(card_id)

                fill_game_card(game_name, game_desc, card_id)
            continue

        if card_desc == '':
            create_media_selector(card_id, games)
            continue


def create_film_desc(film):
    '''
        Create descrition for the film
    '''
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
    return desc


def fill_film_card(card_id, film):
    desc = create_film_desc(film)

    add_desc(card_id, desc)

    draw_imdb_rating(film['imdb'], film['genres'], film['year'])
    add_image_to_card(card_id, 'img/imdb.png')
    add_card_name(card_id, film['title'])


def fill_films_list(list_id):
    cards = get_cards(list_id)

    for card in cards:
        card_name = card['name']
        card_id = card['id']
        card_desc = card['desc']
        films = get_film_names(card_name)
        checklist = get_checklists_id(card_id)

        print(card_name, card_id)

        if len(films) == 1:
            film_name = films[0][0]
            film = find_omdb(film_name, 'movie')

            if film:
                fill_film_card(card_id, film)
            else:
                add_desc(card_id, '# Can not find film with this title')
            continue

        if len(checklist) > 0:
            selected = check_if_item_selected(checklist[0])
            if selected:
                film_name = selected.split('** - ')[0].replace('**', '')
                film = find_omdb(film_name, 'movie')

                if film:
                    fill_film_card(card_id, film)
                    delete_all_checklists(card_id)
                else:
                    add_desc(card_id, '# Can not find film with this title')
                    delete_all_checklists(card_id)
                    create_media_selector(card_id, films)

            continue

        if card_desc == '':
            create_media_selector(card_id, films)

        # film = find_omdb(card_name, t)
        # if not film:
        #     add_desc(card_id, '# Can not find film with this title')
        # else:
        #     desc = create_film_desc(film)
        #     add_desc(card_id, desc)

        #     draw_imdb_rating(film['imdb'], film['genres'], film['year'])
        #     add_image_to_card(card_id, 'img/imdb.png')
        #     add_card_name(card_id, film['title'])


def fill_list(list_id, t):
    cards = get_cards(list_id)

    for card in cards:
        card_name = card['name']
        card_id = card['id']
        print(card_name, card_id)

        film = find_omdb(card_name, t)
        if not film:
            add_desc(card_id, '# Can not find film with this title')
        else:
            film_title = film['title']
            film_year = film['year']
            film_raiting = film['imdb']
            film_plot = film['plot']
            film_genres = film['genres']

            trailers = get_trailer(film_title)
            trailer1_title = trailers[0]['title']
            trailer1_link = trailers[0]['link']
            trailer1_img = trailers[0]['img']
            trailer2_title = trailers[1]['title']
            trailer2_link = trailers[1]['link']
            trailer2_img = trailers[1]['img']

            desc = f'# **{film_title}**  \n---  \n### Year: {film_year}  \n### IMDb raiting: **{film_raiting}**  \n---  \n{film_plot}  \n  \n---  \n### *{trailer1_title}*  \n[![TRAILER 1]({trailer1_img})]({trailer1_link})  \n---  \n### *{trailer2_title}*  \n[![TRAILER 1]({trailer2_img})]({trailer2_link})'
            add_desc(card_id, desc)
            draw_imdb_rating(film_raiting, film_genres, film_year)
            add_image_to_card(card_id, 'img/imdb.png')
            add_card_name(card_id, film_title)


def add_image_to_card(card_id, img_path='img/image.png'):
    files = {'file': open(img_path, 'rb')}

    url = f"https://api.trello.com/1/cards/{card_id}/attachments"
    querystring = {
        "key": f"{TRELLO_KEY}",
        "token": f"{TRELLO_TOKEN}"}

    response = requests.request(
        "POST", url, params=querystring, files=files)

    return json.loads(json.dumps(response.json()))


def add_metacritic_image(game_name, card_id):
    scores = get_metacritic_score(game_name)

    if not scores:
        return None

    user_score = scores['user score']
    critic_score = scores['critic score']
    genres = scores['genres']

    draw_metacritic_image(user_score, critic_score, genres)
    add_image_to_card(card_id)


def update():
    fill_films_list(FILMS_LIST_ID)
    fill_list(SERIES_LIST_ID, 'series')
    fill_games()


if __name__ == '__main__':
    # fill_list(SERIES_LIST_ID, 'series')
    # fill_list(FILMS_LIST_ID, 'movie')
    # fill_games()
    fill_films_list(FILMS_LIST_ID)

    # update()
