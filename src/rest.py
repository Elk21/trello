from flask import Flask, request
from main import update
app = Flask(__name__)


@app.route('/trello', methods=['POST', 'GET'])
def run_update():
    print('*' * 20)
    update()
    return "OK"


if __name__ == '__main__':
    app.run(debug=True)
