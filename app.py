from boggle import Boggle
from flask import Flask, redirect, render_template, request, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

boggle_game = Boggle()

@app.route('/')
def show_board():
    board = boggle_game.make_board()
    session['board'] = board
    high_score = session.get('high_score', 0)
    played = session.get('played', 0)
    return render_template('index.html', high_score = high_score, played = played)

@app.route('/', methods=['POST'])
def check_guess():
    guess_request = request.get_json()
    guess = guess_request['guess']
    result = boggle_game.check_valid_word(session['board'], guess)
    return jsonify(result)

@app.route('/high_score', methods=['POST'])
def high_score():
    score = request.json['score']
    high_score = session.get('high_score', 0)
    played = session.get('played', 0)
    session['played'] = played + 1
    session['high_score'] = max(high_score, score)
    return jsonify(new_score = score > high_score)
