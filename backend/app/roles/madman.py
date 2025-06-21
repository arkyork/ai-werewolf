from .role import Role
from .align_format import fomart_others
from .data.madman import Madman_Prompt
class Madman(Role):
    def __str__(self):
        return "MADMAN"
    def __init__(self):
        self.create = Madman_Prompt()
    def role_play_prompt(self):
        pass  

    def react_prompt_en(self, victim):
        prompt = (
            f"You are the Madman in the game Werewolf. You are secretly helping the Werewolves, but you pretend to be a Villager. "
            f"A villager named {victim} has just been killed. React in a dramatic and emotional way like a panicked villager. "
            f"Do NOT reveal your true role. Just act like a shocked villager.\n"
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
