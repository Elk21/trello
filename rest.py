from flask import Flask, request
from src.main import update
from src.trello import delete_all_webhooks, create_webhooks_for_lists

app = Flask(__name__)


@app.route('/trello', methods=['POST', 'GET'])
def run_update():
    print('*' * 20)
    update()
    return "OK"


if __name__ == '__main__':
    delete_all_webhooks()
    create_webhooks_for_lists()
    app.run(debug=True)
