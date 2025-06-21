from .role import Role
from .align_format import fomart_others

from .data.fox import Fox_Prompt

class Fox(Role):
    def __str__(self):
        return "FOX"
    def __init__(self):
        self.create = Fox_Prompt()
    def role_play_prompt(self):
        pass
    def react_prompt_en(self, victim):
        return (
            "You are secretly a fox in the game Werewolf, pretending to be a villager. "
            f"{victim} has just been killed. "
            "React with one natural sentence showing surprise or sadness, while hiding your true role.\n"
        )

    def react_prompt_ja(self, victim):
        return self.create.react_prompt(victim)

    def sus_prompt_en(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return self.create.sus_play_prompt_en(victim,others)

    def sus_prompt_ja(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return self.create.sus_play_prompt_ja(victim,others)
