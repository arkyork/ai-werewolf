from .role import Role
from .align_format import fomart_others
from .data.medium import Medium_Prompt
class Medium(Role):
    def __str__(self):
        return "MEDIUM"
    def __init__(self):
        self.create = Medium_Prompt()
        
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
        return self.create.react_prompt(victim)

    def sus_prompt_en(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return self.create.sus_play_prompt_en(victim,others)

    def sus_prompt_ja(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return self.create.sus_play_prompt_ja(victim,others)
