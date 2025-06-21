from .role import Role
from .align_format import fomart_others

from .data.wolf import Werewolf_Prompt

class Wolf(Role):
    def __str__(self):
        return "WEREWOLF"
    def __init__(self):
        self.create = Werewolf_Prompt()
    def role_play_prompt(self,candidates):

        messages = [
            {
                "role": "system",
                "content": (
                    f"You are the 'Werewolf' in the game of Werewolf.\n"
                    f"Tonight, you must choose one person to attack.\n"
                    f"The following {len(candidates)} people are the candidates: {', '.join(candidates)}.\n"
                    f"You must select exactly one person from this list.\n"
                    "You do not need to explain your choice. Just reply with a single word: the name.\n"
                    "Do not include any other text, explanation, or names outside of the candidates."
                )
            }
        ]

        return messages
    def role_play_prompt_ja(self, candidates):

        prompt = (
            "あなたは人狼ゲームにおける『人狼』です。\n"
            "今夜、あなたは以下の人物の中から1人を襲撃してください：\n"
            f"{', '.join(candidates)}\n"
            "候補者の名前のみを返信してください。理由やその他のテキストは書かないでください。"
        )

        return prompt


    def react_prompt_en(self,victim):
        prompt = (
            f"You are a villager in the game Werewolf. One of your fellow villagers, {victim}, has just been killed. React in a single natural sentence, as if you were a real person in panic. Don't explain or analyze—just react emotionally as a scared villager.\n"
        )
        return prompt
    
    
    def react_prompt_ja(self, victim):
        return self.create.react_prompt(victim)

    def sus_prompt_en(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return self.create.sus_play_prompt_en(victim,others)

    def sus_prompt_ja(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return self.create.sus_play_prompt_ja(victim,others)