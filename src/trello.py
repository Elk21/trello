import json
import requests
from src.config import TRELLO_TOKEN, TRELLO_KEY

BOARD_ID = 'WIopiWu2'


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


def add_desc(card_id, desc):
    '''
        Put description to a card
    '''

    url = f"https://api.trello.com/1/cards/{card_id}/"
    querystring = {
        "desc": f"{desc}",
        "key": f"{TRELLO_KEY}",
        "token": f"{TRELLO_TOKEN}"}

    response = requests.request("PUT", url, params=querystring)
    return response.json()


def add_card_name(card_id, name):
    '''
        Change name of the card
    '''

    url = f"https://api.trello.com/1/cards/{card_id}/"
    querystring = {
        "name": f"{name}",
        "key": f"{TRELLO_KEY}",
        "token": f"{TRELLO_TOKEN}"}

    response = requests.request("PUT", url, params=querystring)
    return json.loads(json.dumps(response.json()))


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


def delete_all_checklists(card_id):
    '''
        Delete all checklists from card by given card id
    '''

    querystring = {"key": TRELLO_KEY, "token": TRELLO_TOKEN}
    ids = get_checklists_id(card_id)

    for id in ids:
        url = f"https://api.trello.com/1/cards/{card_id}/checklists/{id}"
        response = requests.request("DELETE", url, params=querystring)
    # return response.text
