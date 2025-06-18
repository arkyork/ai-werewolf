from .role import Role
from .others import fomart_others
class Villager(Role):
    def __str__(self):
        return "VILLAGER"
    def role_play_pormpt(self):
        pass
    def react_prompt_en(self,victim):
        prompt = (
            f"You are a werewolf pretending to be a villager in the game Werewolf. Just now, a villager named {victim} was killed. Pretend to be shocked and scared, and say one panicked sentence like a human would. Do not explain your role—just act like a villager in emotional distress.\n"
        )

        return prompt
    

    
    def sus_prompt_en(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)

        prompt = (
            f"You are a participant in the game of Werewolf. Your role is a Villager.\n"
            f"Below are examples of other people's reactions when the villager {victim} was killed.\n"
            f"{others}\n"
            f"Based on these reactions, emotionally express who seems suspicious.\n"
        )
        return prompt


    def react_prompt_ja(self,victim):
        prompt =  (
                    "以下は人狼ゲームで村人が殺されたときの、他の村人の反応の例です。\n"
                    "えっ！？なんであの人が……！僕じゃないよ、信じて！\n"
                    "こ、怖い……ち、違うってば……！私じゃないから……！\n"
                    f"{victim} が殺された直後の村人としての反応を、1文で出力してください。\n"
                )
        
        return prompt

    def sus_prompt_ja(self,victim,me,kill_reactionss):

        others = fomart_others(kill_reactionss,me)
        
        prompt = (
            f"あなたは人狼ゲームの参加者です。役割は村人です。\n"
            f"以下は村人{victim}が殺されたときの、別の人の反応の例です。\n"
            f"{others}"
            f"これらの反応から誰が怪しいか感情豊かに出力してください。\n"
        )
        return prompt