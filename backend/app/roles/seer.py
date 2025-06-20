from .role import Role
from .align_format import fomart_others

import random

class Seer(Role):
    def __str__(self):
        return "SEER"

    def role_play_prompt(self, candidates,seer_name):

        candidates = list(set(candidates)-set([seer_name]))
        random.shuffle(candidates)
        
        messages = [
            {
                "role": "system",
                "content": (
                    f"You are the 'Seer' in the game of Werewolf.\n"
                    f"Tonight, you may divine the true role of one person.\n"
                    f"The following {len(candidates)} people are the candidates: {', '.join(candidates)}.\n"
                    f"You must select one person from this list to divine their role.\n"
                    "Just reply with a single name from the candidates. Do not explain your choice or include any other text."
                )
            }
        ]
        return messages
    def role_play_prompt_ja(self, candidates, seer_name):

        candidates = list(set(candidates) - set([seer_name]))
        random.shuffle(candidates)

        prompt = (
            "以下の人物の中から1人だけ選び、その人物の正体を占いなさい。\n"
            f"候補者：{', '.join(candidates)}\n"
            "候補者の名前だけを返信せよ。他の説明は一切不要。"
        )

        return prompt

    def react_prompt_en(self, victim):
        return (
            "You are a villager in the game Werewolf."
            f"One of your fellow villagers, {victim}, has just been killed."
            "React in a single natural sentence as if you were a real person in panic. "
            "Don't explain or analyze—just react emotionally as a scared villager.\n"
        )

    def react_prompt_ja(self, victim):
        return (
            "あなたは人狼ゲームの占い師です。"
            f"仲間の村人である {victim} が殺されました。現実の人間のようにパニックになって、自然な1文で感情的に反応してください。"
            "説明や分析はせず、怖がっている村人として感情を表現してください。\n"
        )

    def sus_prompt_en(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return (
            f"You are a participant in the game of Werewolf. Your role is the Seer.\n"
            f"The villager {victim} was killed.\n"
            f"Here are the reactions of other players:\n{others}\n"
            f"Based on these reactions, emotionally express who you find suspicious.\n"
        )

    def sus_prompt_ja(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return (
            f"あなたは人狼ゲームの参加者で、役職は占い師です。\n"
            f"村人である {victim} が殺されました。\n"
            f"以下は他のプレイヤーの反応の例です：\n{others}\n"
            f"これらの反応から、感情的に誰が怪しいかを出力してください。\n"
        )
