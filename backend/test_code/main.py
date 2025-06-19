from flask import Flask, jsonify,request

app = Flask(__name__)



@app.route("/kill", methods=["GET"])
def get_reaction():
    data = {
    "alive": [
        "さぶろう", "しんじ", "けんた", "ゆうこ",
        "あかね", "みさき", "りょう", "はるか"
    ],
    "bread_num": 1,
    "die_role": "llama-3.1 -> VILLAGER",
    "divine_role": "失敗",
    "kill_reactions": {
        "あかね": "あああ、神様、嘘でしょ?!なんで、 なんで！なんでウテイが殺されなきゃならないの?!...",
        "けんた": "わあああ、誰がやったの?!なんで、 なんで殺されたの?!...",
        "さぶろう": "「嘘つきが殺された！」村人Aが叫んだ。...",
        "しんじ": "「うそでしょ……なんで、たかしさんが……」",
        "はるか": "「なんで、また殺されたの?!もう、信じられない!!」",
        "みさき": "「ひっ、まさか、まさかだよ、信じられない、誰がこんな酷いことするの⁉」",
        "ゆうこ": "憎い！憎い！なぜ！なぜ殺された！なぜ！なぜ！許せない！...",
    },
    "sus_reactions": {
        "あかね": "けんたとゆうこが感情的に怪しいと判断できます。...",
        "けんた": "あなたは人狼です。以下、反応から感情豊かに誰が怪しいか出力します。...",
        "さぶろう": "しんじの反応は、感情が表面に出ており...",
        "しんじ": "ゆうこが怪しいと出力されました。...",
        "はるか": "※あくまで感情的に判断しています...",
        "みさき": "けんたの反応が一番怪しいと感じます。...",
        "ゆうこ": "けんたは非常に感情的に反応しています。...",
    },
    "victim": ["りょう"]
}

    return jsonify(data)
@app.route("/start", methods=["GET"])
def start():

    data = {
        "あかね": {
            "alive": True,
            "role": "SEER"
        },
        "けんた": {
            "alive": True,
            "role": "WEREWOLF"
        },
        "さぶろう": {
            "alive": True,
            "role": "FOX"
        },
        "しんじ": {
            "alive": True,
            "role": "BAKER"
        },
        "じろう": {
            "alive": True,
            "role": "VILLAGER"
        },
        "たろう": {
            "alive": True,
            "role": "VILLAGER"
        },
        "はるか": {
            "alive": True,
            "role": "MADMAN"
        },
        "みさき": {
            "alive": True,
            "role": "WEREWOLF"
        },
        "ゆうこ": {
            "alive": True,
            "role": "MEDIUM"
        },
        "りょう": {
            "alive": True,
            "role": "KNIGHT"
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
