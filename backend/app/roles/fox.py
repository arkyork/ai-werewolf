from .role import Role
from .align_format import fomart_others

class Fox(Role):
    def __str__(self):
        return "FOX"
    def role_play_prompt(self):
        pass
    def react_prompt_en(self, victim):
        return (
            "You are secretly a fox in the game Werewolf, pretending to be a villager. "
            f"{victim} has just been killed. "
            "React with one natural sentence showing surprise or sadness, while hiding your true role.\n"
        )

    def react_prompt_ja(self, victim):
        return (
            "あなたは人狼ゲームの妖狐です（村人のふりをしています）。"
            f"{victim} が殺されました。"
            "自分の正体を隠しつつ、驚きや悲しみを装って自然な1文で反応してください。\n"
        )

    def sus_prompt_en(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return (
            f"You are secretly the fox in the game of Werewolf, pretending to be a villager.\n"
            f"The villager {victim} has been killed.\n"
            f"Here are the reactions of the others:\n{others}\n"
            f"While maintaining your cover, emotionally express who you find suspicious.\n"
        )

    def sus_prompt_ja(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        return (
            f"あなたは人狼ゲームの妖狐です（村人のふりをしています）。\n"
            f"村人である {victim} が殺されました。\n"
            f"以下は他のプレイヤーの反応です：\n{others}\n"
            f"自分の正体を隠しながら、感情的に誰が怪しいかを出力してください。\n"
        )
