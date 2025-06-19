from .role import Role
from .align_format import fomart_others

class Baker(Role):
    def __str__(self):
        return "BAKER"
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
        return (
            "あなたは人狼ゲームのパン屋です。"
            f"仲間の村人である {victim} が殺されました。現実の人間のようにショックと悲しみを込めて自然な1文で反応してください。"
            "説明はせず、友達を失ったパン屋として感情的に反応してください。\n"
        )

    def sus_prompt_en(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return (
            f"You are a baker in the game of Werewolf.\n"
            f"The villager {victim} has been killed.\n"
            f"Here are the reactions of the others:\n{others}\n"
            f"Based on these reactions, emotionally express who you find suspicious.\n"
        )

    def sus_prompt_ja(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return (
            f"あなたは人狼ゲームのパン屋です。\n"
            f"村人である {victim} が殺されました。\n"
            f"以下は他のプレイヤーの反応です：\n{others}\n"
            f"これらの反応から、感情的に誰が怪しいかを出力してください。\n"
        )
