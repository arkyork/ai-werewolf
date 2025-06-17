from .role import Role

class Wolf(Role):
    def __str__():
        return "WEREWOLF"
    
    def react_prompt(self,victim):
        prompt = (
            f"You are a villager in the game Werewolf. One of your fellow villagers, {victim}, has just been killed. React in a single natural sentence, as if you were a real person in panic. Don't explain or analyze—just react emotionally as a scared villager.\n"
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

