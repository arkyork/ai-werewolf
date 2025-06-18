from .role import Role
from .others import fomart_others

class Wolf(Role):
    def __str__(self):
        return "WEREWOLF"
    
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
    def react_prompt_en(self,victim):
        prompt = (
            f"You are a villager in the game Werewolf. One of your fellow villagers, {victim}, has just been killed. React in a single natural sentence, as if you were a real person in panic. Don't explain or analyze—just react emotionally as a scared villager.\n"
        )
        return prompt
    
    
    def react_prompt_ja(self,victim):
        prompt = (
            f"あなたは人狼ゲームの村人です。仲間の村人である {victim} が殺されました。現実の人間のようにパニックになって、自然な1文で感情的に反応してください。説明や分析はせず、怖がっている村人として感情を表現してください。\n"
        )
        return prompt


    def sus_prompt_ja(self,victim,me,kill_reactionss):

        others = fomart_others(kill_reactionss,me)

        prompt =  (
            f"あなたは人狼ゲームの参加者です。役割は人狼です。\n"
            f"あなたは人狼として村人{victim}を殺しました。\n"
            f"以下は村人{victim}が殺されたときの、別の人の反応の例です。\n"
            f"{others}"
            f"絶対に人狼であるとばれないように村人としてふるまってください。\n"
            f"これらの反応から感情豊かに誰が怪しいか出力してください。\n"
        )
        return prompt
    def sus_prompt_en(self, victim, me, kill_reactionss):
        others = fomart_others(kill_reactionss, me)

        prompt = (
            f"You are a participant in the game of Werewolf. Your role is a Werewolf.\n"
            f"You, as the Werewolf, killed the villager {victim}.\n"
            f"Here are examples of other people's reactions when the villager {victim} was killed:\n"
            f"{others}\n"
            f"Act as a villager so that no one suspects you are the Werewolf—do not get caught.\n"
            f"Emotionally express who seems suspicious based on these reactions.\n"
        )
        return prompt
