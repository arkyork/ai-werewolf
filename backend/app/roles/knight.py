from .role import Role
from .align_format import fomart_others
import random

class Knight(Role):
    def __str__(self):
        return "KNIGHT"

    def role_play_prompt(self, candidates, knight_name):
        candidates = list(set(candidates) - set([knight_name]))  # 自分以外を候補に
        random.shuffle(candidates)

        return [
            {
                "role": "system",
                "content": (
                    f"You are the 'Knight' in the game of Werewolf.\n"
                    f"Tonight, you can choose one person to protect.\n"
                    f"The following {len(candidates)} people are the candidates: {', '.join(candidates)}.\n"
                    "Please reply with one name only from the list. Do not explain your choice or add any extra text."
                )
            }
        ]

    def role_play_prompt_ja(self, candidates, knight_name):
        candidates = list(set(candidates) - set([knight_name]))
        random.shuffle(candidates)

        prompt = (
            "system: あなたは人狼ゲームの騎士です。\n"
            f"今夜は以下の人物のうち1人を護衛することができます：{', '.join(candidates)}。\n"
            "リストの中から1人だけ名前を返してください。理由や説明は不要です。余計な文章は含めないでください。"
        )

        return prompt

    def react_prompt_en(self, victim):
        return (
            "You are the knight in the game Werewolf. "
            f"{victim}, someone you swore to protect, was just killed. "
            "React with a single emotional sentence. Do not explain or analyze—just show raw emotion.\n"
        )

    def react_prompt_ja(self, victim):
        return (
            "あなたは人狼ゲームの騎士です。"
            f"護るべき仲間である {victim} が殺されました。"
            "現実の人間のように感情的に1文で反応してください。説明や分析はせず、悲しみや悔しさを表現してください。\n"
        )

    def sus_prompt_en(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return (
            f"You are the knight in the game of Werewolf.\n"
            f"The villager {victim} has been killed.\n"
            f"Here are the reactions of the others:\n{others}\n"
            f"Based on these reactions, emotionally express who you find suspicious.\n"
        )

    def sus_prompt_ja(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return (
            f"あなたは人狼ゲームの騎士です。\n"
            f"村人である {victim} が殺されました。\n"
            f"以下は他のプレイヤーの反応です：\n{others}\n"
            f"これらの反応から、感情的に誰が怪しいかを出力してください。\n"
        )
