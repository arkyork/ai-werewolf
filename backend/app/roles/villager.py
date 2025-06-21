from .role import Role
from .align_format import fomart_others
from .data.villager import Villager_Prompt
class Villager(Role):
    def __str__(self):
        return "VILLAGER"
    def __init__(self):
        self.create = Villager_Prompt()
    def role_play_prompt(self):
        pass
    def react_prompt_en(self,victim):
        prompt = (
            f"You are a werewolf pretending to be a villager in the game Werewolf. Just now, a villager named {victim} was killed. Pretend to be shocked and scared, and say one panicked sentence like a human would. Do not explain your role—just act like a villager in emotional distress.\n"
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

