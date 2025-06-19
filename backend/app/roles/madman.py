from .role import Role
from .align_format import fomart_others

class Madman(Role):
    def __str__(self):
        return "MADMAN"

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
        prompt = (
            "あなたは人狼ゲームの『狂人』です。人狼の味方ですが、村人のふりをしています。\n"
            f"今、村人の{victim}が殺されました。\n"
            "パニックになっている村人のように、感情的な一文を出力してください。ただし、自分の正体を明かしてはいけません。\n"
        )
        return prompt

    def sus_prompt_en(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        prompt = (
            f"You are the Madman in the game of Werewolf. You pretend to be a Villager, but secretly support the Werewolves.\n"
            f"The villager {victim} has just been killed. Below are the reactions of other players:\n"
            f"{others}\n"
            "Based on these reactions, emotionally accuse someone who looks suspicious. "
            "Try to protect the real Werewolves if you can.\n"
        )
        return prompt

    def sus_prompt_ja(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)
        prompt = (
            "あなたは人狼ゲームの『狂人』です。村人のふりをしていますが、密かに人狼を助ける役目です。\n"
            f"今、村人の{victim}が殺されました。以下は他の参加者の反応です。\n"
            f"{others}"
            "この反応をもとに、感情的に誰が怪しいかを出力してください。\n"
            "※可能であれば人狼をかばってください。\n"
        )
        return prompt
