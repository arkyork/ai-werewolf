from .role import Role
from .align_format import fomart_others

from .data.baker import Baker_Prompt

# パン屋
class Baker(Role):
    def __str__(self):
        return "BAKER"
    def __init__(self):
        self.create=Baker_Prompt()
    def role_play_prompt(self):
        pass
    def react_prompt_en(self, victim):
        return (
            "You are a baker in the game Werewolf. "
            f"The villager {victim} was just killed. "
            "React with a single natural sentence as if you're a real person in shock and grief. "
            "Don't explain anything—just emotionally respond like a baker who lost a friend.\n"
        )

    def react_prompt_ja(self, victim):
        return self.create.react_prompt(victim)

    def sus_prompt_en(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return self.create.sus_play_prompt_en(victim,others)

    def sus_prompt_ja(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return self.create.sus_play_prompt_ja(victim,others)
