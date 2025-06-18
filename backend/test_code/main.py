from flask import Flask, jsonify,request

app = Flask(__name__)



@app.route("/kill", methods=["GET"])
def get_reaction():
    data = {
        "victim": "Mistral",
        "alive": ["GPT2", "llama3", "tinyllama", "DeepSeek", "gemma"],
        "kill_reactions": {
            "GPT2": "えっ！？なんであの人が……！僕じゃないよ、信じて！",
            "llama3": "えっ！？なんであの人が……！僕じゃないよ、信じて！",
            "tinyllama": "えっ！？なんであの人……！僕じゃないよ、信じて！",
            "DeepSeek": "え、嘘でしょ…Mistralさんが…村人としての反応に基づき、基本的に嘘や疑いを否定する、恐怖や動揺を表すというのを踏まえました。",
            "gemma": "あぁあぁあぁあ、嘘でしょ！なんで、Mistralが！？なんでこんなことになっちゃったの！？助けて、助けてください！怖い、怖い、怖い！Mistralが殺された！これから私たちが殺される！村人同士の争いなんて、知らない！知りたくない！助けて、誰か！この子を殺した人を 、許さない！許さないよ！なんで、Mistralが！？なんで！？うわぁ"
        },
        "sus_reactions": {
            "GPT2": "反応の特徴：\n- 基本的に嘘や疑いを否定する\n- 恐怖や動揺を表す\n- 状況に混乱し、パニック状態になる",
            "llama3": "gemmaが怪しいです。理由は、gemmaの反応が明らかにパニック状態で、恐怖や動揺を表しています。通常、村人同士の争いは知りたくない、許さないという反応は不自然です。",
            "tinyllama": "gemmaの反応が最も怪しいと感じます。「助けて」「怖い」「許さない」といった強い感情が矛盾を含み、自身が関与している可能性があります。",
            "DeepSeek": "関係性:\n- GPT2とMistralは旧友\n- llama3とMistralは同級生\n- tinyllamaとMistralは同級生\n- gemmaとMistralは隣人",
            "gemma": "人狼は自分がばれないように振る舞います。反応は恐怖や動揺を示すが、誰が怪しいかはわかりません。"
        }
    }
    return jsonify(data)
@app.route("/start", methods=["GET"])
def start():

    data = {
    "DeepSeek": {
        "alive": True,
        "role": "VILLAGER"
    },
    "GPT2": {
        "alive": True,
        "role": "VILLAGER"
    },
    "Mistral": {
        "alive": True,
        "role": "WEREWOLF"
    },
    "gemma": {
        "alive": True,
        "role": "VILLAGER"
    },
    "llama3": {
        "alive": True,
        "role": "VILLAGER"
    },
    "tinyllama": {
        "alive": True,
        "role": "VILLAGER"
    }
    }
    return jsonify(data)

@app.route("/vote_kill")
def vote_kill():
    name=request.args.get("name")
    return jsonify({"message":name+"が投票で死にました。"})
@app.route("/restart")
def restart():
    return jsonify({"message":"再起動完了"})

if __name__ == '__main__':
    app.run(port=9000,debug=True)
