from flask import Flask, request
from main import update
app = Flask(__name__)


@app.route('/trello', methods=['POST'])
def run_update():
    update()
    return "OK"


if __name__ == '__main__':
    app.run(debug=True, host='https://intense-harbor-83800.herokuapp.com')
