from game.game_ja import Wolf_JA
from game.game_en import Wolf_EN

from flask import Flask,jsonify
from flask import request

import torch
import gc

app = Flask(__name__)
game = None


def clear():
    global game
    del game
    gc.collect()

    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()

    game = None


@app.route("/restart")
def restart():
    clear()
    return jsonify({"message":"再起動完了"})

@app.route("/lang")
def lang():
    global game
    if game is not None:
        clear()

    if request.args.get("lang") == "en":
        game = Wolf_EN()
    if request.args.get("lang") == "ja":
        game = Wolf_JA()


@app.route("/start")
def start():
    global game

    if game is not None:
        clear()

    
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
    
    json_data={
        "victim":data[0],
        "alive":data[1],
        "kill_reactions":data[2],
        "sus_reactions":data[3],

    }

    return jsonify(json_data)

@app.route("/vote_kill")
def vote_kill():
    name=request.args.get("name")
    game.vote_kill(name)


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)

