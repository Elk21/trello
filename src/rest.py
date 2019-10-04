from flask import Flask, request
app = Flask(__name__)


@app.route('/trello', methods=['POST'])
def sendgrid_parser():

    return "OK"


if __name__ == '__main__':
    app.run(debug=True)
