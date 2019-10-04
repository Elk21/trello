import requests
TRELLO_KEY = 'a2c44f7078a2585af30d658cef7287a3'
TRELLO_TOKEN = '25f4b79910f15728b2c19ecc4aa86aebbd0c0ae3d0e66d1ce5bdfa6c5a9a530a'
CALLBACK_URL = "https://quiet-ridge-13488.herokuapp.com/trello"


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


def create_webhook(idModel):
    '''
        Create webhook for object with <idModel>
    '''
    url = f"https://api.trello.com/1/tokens/{TRELLO_TOKEN}/webhooks/"
    querystring = {"key": TRELLO_KEY,
                   "callbackURL": CALLBACK_URL,
                   "idModel": f"{idModel}",
                   "description": "Some webhook"}
    response = requests.request("POST", url, params=querystring)
    print('created hook ', response.text)

    return response


# create_webhook('4d5ea62fd76aa1136000000c')
# print(get_webhooks())
# delete_webhook('4d5ea62fd76aa1136000000c')
delete_all_webhooks()
