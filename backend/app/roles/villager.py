from .role import Role

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
        