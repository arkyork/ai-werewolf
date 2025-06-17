from game.game_ja import Wolf_JA
from game.game_en import Wolf_EN

from flask import Flask
from flask import request

app = Flask(__name__)
game = None

@app.route("/lang")
def lang():
    global game
    if request.args.get("lang") == "en":
        game = Wolf_EN()
    if request.args.get("lang") == "ja":
        game = Wolf_JA()


@app.route("/kill")
def kill():
    game.kill()


@app.route("/vote")
def kill():
    game.kill()


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)
    game = Wolf_JA()

