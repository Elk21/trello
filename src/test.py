import requests
TRELLO_KEY = 'a2c44f7078a2585af30d658cef7287a3'
TRELLO_TOKEN = '25f4b79910f15728b2c19ecc4aa86aebbd0c0ae3d0e66d1ce5bdfa6c5a9a530a'
CALLBACK_URL = "https://quiet-ridge-13488.herokuapp.com/trello"
BOARD_ID = 'WIopiWu2'


def get_webhooks():
    '''

    '''

    url = f"https://api.trello.com/1/tokens/{TRELLO_TOKEN}/webhooks"
    querystring = {"key": TRELLO_KEY}
    response = requests.request("GET", url, params=querystring)

    ar = []
    for x in response.json():
        ar.append({'id': x['id'], 'idModel': x['idModel']})

    return ar


def delete_webhook(idModel):
    '''
        Delete webhook
    '''

    hooks = get_webhooks()
    for hook in hooks:
        if idModel == hook['idModel']:
            webhook_id = hook['id']
            url = f"https://api.trello.com/1/tokens/{TRELLO_TOKEN}/webhooks/{webhook_id}"
            querystring = {"key": TRELLO_KEY}
            response = requests.request("DELETE", url, params=querystring)
            print('deleted ', response.text)
            return response.text
        else:
            return None


def delete_all_webhooks():
    '''
        Delete webhooks
    '''

    hooks = get_webhooks()
    for hook in hooks:
        webhook_id = hook['id']
        url = f"https://api.trello.com/1/tokens/{TRELLO_TOKEN}/webhooks/{webhook_id}"
        querystring = {"key": TRELLO_KEY}
        response = requests.request("DELETE", url, params=querystring)
        print('deleted ', response.text)
    # return response.text


def create_webhook(idModel, desc="Some webhook"):
    '''
        Create webhook for object with <idModel>
    '''

    url = f"https://api.trello.com/1/tokens/{TRELLO_TOKEN}/webhooks/"
    querystring = {"key": TRELLO_KEY,
                   "callbackURL": CALLBACK_URL,
                   "idModel": f"{idModel}",
                   "description": desc}
    response = requests.request("POST", url, params=querystring)
    print('created hook ', response.text)

    return response.text


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
    return response.json()


def create_webhooks_for_lists():
    lists = get_lists()

    for x in lists:
        create_webhook(x['id'], x['name'])


create_webhooks_for_lists()
# print(get_lists())
# create_webhook('5d70c3692f0fe53b6fa1858f')
print(get_webhooks())
# delete_webhook('4d5ea62fd76aa1136000000c')
# delete_all_webhooks()
