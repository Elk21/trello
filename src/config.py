YOUTUBE_TOKEN = 'AIzaSyBplMZXvkzWctymn5L-1Jh6T3IG5wp0e5k'
OMDB_TOKEN = '2f27933'
TRELLO_KEY = 'a2c44f7078a2585af30d658cef7287a3'
TRELLO_TOKEN = '25f4b79910f15728b2c19ecc4aa86aebbd0c0ae3d0e66d1ce5bdfa6c5a9a530a'


curl - X POST - H "Content-Type: application/json" \
    https: // api.trello.com/1/tokens/a2c44f7078a2585af30d658cef7287a3/webhooks / \
    -d '{
        "key": "a2c44f7078a2585af30d658cef7287a3",
        "callbackURL": "https://intense-harbor-83800.herokuapp.com/trello",
        "idModel": "4d5ea62fd76aa1136000000c",
        "description": "My first webhook"
    }'
