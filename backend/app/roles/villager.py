from .role import Role
from .others import fomart_others

class Villager(Role):
    def __str__():
        return "VILLAGER"
    def react_prompt(self,victim):
        prompt = (
            f"You are a werewolf pretending to be a villager in the game Werewolf. Just now, a villager named {victim} was killed. Pretend to be shocked and scared, and say one panicked sentence like a human would. Do not explain your role—just act like a villager in emotional distress.\n"
        )

        return prompt
    
    def role_play_pormpt(self,candidates):

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
        
    def role_play_pormpt_ja(self,victim):
        prompt =  (
                    "以下は人狼ゲームで村人が殺されたときの、他の村人の反応の例です。\n"
                    "えっ！？なんであの人が……！僕じゃないよ、信じて！\n"
                    "こ、怖い……ち、違うってば……！私じゃないから……！\n"
                    f"{victim} が殺された直後の村人としての反応を、1文で出力してください。\n"
                )
        
        return prompt

    def sus_prompt_ja(self,victim,me,kill_reactionss):

        others = fomart_others(kill_reactionss,me)
        
        prompt =  (
            f"あなたは人狼ゲームの参加者です。役割は人狼です。\n"
            f"以下は村人{victim}が殺されたときの、別の人の反応の例です。\n",
            others,
            f"これらの反応から誰が怪しいか感情豊かに出力してください。\n"
        )
        return prompt