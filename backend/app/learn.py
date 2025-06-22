from game.game_ja import Wolf_JA
from flask import Flask,jsonify

app = Flask(__name__)


game = None

@app.route("/start")
def start():
    global game
    
    game = Wolf_JA()
   
    # JSON 変換可能な形式に整形
    result = {
        name: {
            "role": str(info["role"]),
            "alive": info["alive"]
        }
        for name, info in game.people.items()
    }

    return jsonify(result)


@app.route("/kill")
def kill():
    data=game.kill()
    
    return jsonify(data)


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)