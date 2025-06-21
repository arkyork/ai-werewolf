from .role import Role
from .align_format import fomart_others
from .data.seer import Seer_Prompt
import random

class Seer(Role):
    def __str__(self):
        return "SEER"
    def __init__(self):
        self.create = Seer_Prompt()

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
        return self.create.react_prompt(victim)

    def sus_prompt_en(self, victim, me, kill_reactionss,result):
        others = fomart_others(kill_reactionss, me)
        return self.create.sus_play_prompt_en(victim,others,result)

    def sus_prompt_ja(self, victim, me, kill_reactionss,result):
        others = fomart_others(kill_reactionss, me)
        return self.create.sus_play_prompt_ja(victim,others,result)

