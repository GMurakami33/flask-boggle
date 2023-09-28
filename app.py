
from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "123987"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def home():
    """Render Boggle gameboard and show form"""
    session['board'] = boggle_game.make_board()
    session['score'] = 0
    highscore = session.get("highscore", 0)
    tries = session.get("tries", 0)
    guessed_words = session.get('guessed_words', [])  
    return render_template('index.html', highscore=highscore, tries=tries, guessed_words=guessed_words)

@app.route('/check-word', methods=['POST'])
def check_word():
    """Check if the submitted word is valid"""
    word = request.json['word']
    board = session['board']
    guessed_words = session.get('guessed_words', []) 

    if word not in guessed_words:
        result = boggle_game.check_valid_word(board, word)
        if result == "ok":
            if 'score' not in session:
                session['score'] = 0
            guessed_words.append(word)
            session['score'] += len(word)
        session['guessed_words'] = guessed_words
    else:
        result = "duplicate-word"

    highscore = session.get('highscore', 0)
    tries = session.get('tries', 0)
    session['highscore'] = max(session['score'], highscore)
    session['tries'] = tries + 1 

    return jsonify({'result': result, 'score':session['score']})

if __name__ == '__main__':
    app.run()
