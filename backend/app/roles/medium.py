from .role import Role
from .align_format import fomart_others

class Medium(Role):
    def __str__(self):
        return "MEDIUM"

    def role_play_prompt(self, deads):
        dead_name = ",".join(deads)
        return [
            {
                "role": "system",
                "content": (
                    f"You are the 'Medium' in the game of Werewolf.\n"
                    f"Tonight, you will perform a séance to learn the role of the deceased: {dead_name}.\n"
                    "You will receive the exact role of that person. Just reply with a single word (e.g., 'WEREWOLF', 'VILLAGER', etc.). "
                    "Do not explain or add anything else."
                )
            }
        ]

    def role_play_prompt_ja(self, dead_name):
        prompt = (
            "あなたは人狼ゲームの霊媒師です。\n"
            f"今夜、死亡した {dead_name} の正体を霊視します。\n"
            "その人物の役職を一語で答えてください（例：WEREWOLF、VILLAGER など）。\n"
            "絶対に役職名だけを一語で返答してください。それ以外の解説や文字は一切書かないでください。"
        )
        return prompt


    def react_prompt_en(self, victim):
        return (
            "You are the medium in the game Werewolf. "
            f"The villager {victim} was just killed. "
            "React emotionally with a natural sentence, as if you're a real person who just lost someone in the village. "
            "Don't explain or analyze—just express raw emotion.\n"
        )

    def react_prompt_ja(self, victim):
        return (
            "あなたは人狼ゲームの霊媒師です。"
            f"仲間の村人である {victim} が殺されました。"
            "現実の人間のように感情的な1文で反応してください。説明や分析はせず、感情だけを表現してください。\n"
        )

    def sus_prompt_en(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return (
            f"You are the medium in the game of Werewolf.\n"
            f"The villager {victim} has been killed.\n"
            f"Here are the reactions of the others:\n{others}\n"
            f"Based on these reactions, emotionally express who seems suspicious.\n"
        )

    def sus_prompt_ja(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return (
            f"あなたは人狼ゲームの霊媒師です。\n"
            f"村人である {victim} が殺されました。\n"
            f"以下は他のプレイヤーの反応です：\n{others}\n"
            f"これらの反応から、感情的に誰が怪しいかを出力してください。\n"
        )
