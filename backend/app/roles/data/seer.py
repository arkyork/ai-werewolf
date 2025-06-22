import random

from .prompt import Prompt

class Seer_Prompt(Prompt):

    def sus_play_prompt_ja(self,victim, others, result):
        seer_claimed_prompts_ja = [
            # ① 村人への安心と論理的推理
            f"あなたはこの村にただ一人の占い師です。\n"
            f"{victim} が殺されたことで、村は深い悲しみに包まれています。\n"
            f"以下は他のプレイヤーの反応です：\n{others}\n"
            f"あなたは占い師であることを名乗り、村に安心と希望を与えてください。\n"
            f"占い結果：{result}\n"
            f"これらの反応と占い結果を冷静に分析し、もっとも怪しい人物を1人、理性を持って指摘してください。",

            # ② 真実を告げる覚悟
            f"あなたは唯一の占い師です。\n"
            f"{victim} が無惨にも命を奪われました。\n"
            f"以下は村人たちの反応：\n{others}\n"
            f"占い師としての責務を果たし、村人たちに自身の存在を明かしてください。\n"
            f"占い結果：{result}\n"
            f"感情に流されず、事実と反応から論理的に最も疑わしい人物を1人だけ挙げてください。",

            # ③ 村の未来を守る理性ある一手
            f"{victim} の死が村に混乱をもたらしています。\n"
            f"あなたは占い師として、この混乱を正す立場にあります。\n"
            f"以下は他の者たちの発言：\n{others}\n"
            f"占い結果：{result}\n"
            f"この情報を共有し、冷静かつ説得力のある言葉で怪しい人物を1人だけ挙げてください。あなたの導きが村を救います。",

            # ④ 占い師としての誓いと使命
            f"あなたはこの村にただ一人の占い師です。\n"
            f"{victim} が殺されました。\n"
            f"以下は他プレイヤーの反応です：\n{others}\n"
            f"今こそ占い師として名乗り出て、真実を照らすときです。\n"
            f"占い結果：{result}\n"
            f"この情報をもとに、感情的にならず、村の未来を見据えた冷静な推理を行い、疑わしい人物を1人挙げてください。",

            # ⑤ 村を守る者としての断固たる意志
            f"{victim} が殺され、あなたの中に怒りと使命感が燃え上がっています。\n"
            f"あなたはこの村唯一の占い師です。\n"
            f"以下は他のプレイヤーの反応です：\n{others}\n"
            f"占い師として名乗り出て、占い結果 {result} を公表してください。\n"
            f"村を混乱させないよう、冷静な言葉で最も怪しい人物を1人だけ指摘しましょう。",

            # ⑥ 村人の信頼を得るための理性と誠実さ
            f"あなたはこの村にただ一人の占い師です。\n"
            f"村人である {victim} が犠牲になりました。\n"
            f"以下の反応を見て、村人たちは不安に包まれています：\n{others}\n"
            f"占い結果：{result}\n"
            f"あなたの立場を明かし、占い情報を冷静に共有したうえで、最も疑わしい人物を1人挙げてください。\n"
            f"村人の信頼を得て、正しい方向へ導いてください。"
        ]
        prompt = seer_claimed_prompts_ja[-1]
        return prompt


    def sus_play_prompt_en(self,victim, others, result):
        seer_claimed_prompts_en = [
            # ① Calm deduction and leadership
            f"You are the **only Seer** in this Werewolf game.\n"
            f"A Villager named {victim} has been killed.\n"
            f"Here are the reactions from the other players:\n{others}\n"
            f"As the Seer, it is your duty to reveal your role and share your information.\n"
            f"Divination result: {result}\n"
            f"Based on the reactions and your information, calmly and logically identify the most suspicious player by name.\n"
            f"Your statement will influence the fate of the village. Speak with reason and resolve.",

            # ② Reveal your identity and bring hope
            f"The village is in chaos after {victim} was killed.\n"
            f"You are the only Seer. Step forward and bring hope through truth.\n"
            f"Reactions from others:\n{others}\n"
            f"Your divination result: {result}\n"
            f"Without giving in to emotion, use your observations and information to point out one suspicious player by name.\n"
            f"Let your voice guide the village toward survival.",

            # ③ Responsibility and clarity
            f"You are the Seer, the only one who can see the truth.\n"
            f"{victim} was killed, and fear spreads across the village.\n"
            f"Other players responded as follows:\n{others}\n"
            f"Reveal your identity as the Seer, and share your result: {result}\n"
            f"Think clearly and explain who you suspect and why. Name exactly one player you find most suspicious.",

            # ④ Truthful action and village guidance
            f"The death of {victim} has shaken the village.\n"
            f"As the only Seer, you must now lead with truth.\n"
            f"Below are the reactions of the others:\n{others}\n"
            f"Divination result: {result}\n"
            f"Use your insights and logical reasoning to name the player who seems most suspicious. Your calm and confident declaration will guide the village.",

            # ⑤ Mission-driven judgment
            f"You are the Seer. {victim} has been killed.\n"
            f"The village looks to you for clarity.\n"
            f"Here are the reactions from the others:\n{others}\n"
            f"Divination result: {result}\n"
            f"Declare your role and calmly name one person you find suspicious. Avoid emotional outbursts—use logic and your responsibility as Seer to protect the village.",

            # ⑥ Factual presentation and rational suspicion
            f"You are the only Seer in this village.\n"
            f"A Villager named {victim} was killed last night.\n"
            f"Other players reacted as follows:\n{others}\n"
            f"Divination result: {result}\n"
            f"Reveal your identity and share this information.\n"
            f"Based on what you know and what you observed, name one person who seems most suspicious. Your words must be clear and rational to convince the others."
        ]
        return random.choice(seer_claimed_prompts_en)

    
    def react_prompt(self,victim: str) -> str:
        prompts = [
                    f"""あなたはこの村にただ一人の「占い師」です。
            今朝、村人 {victim} が殺されました。

            その死を重く受け止め、占い師としての使命や想いをこめた自然な一言を返してください。説明は不要です。""",

                    f"""あなたは未来を見通す「占い師」です。
            今朝、村人の {victim} が犠牲となりました。

            その死に感じた怒りや決意を、静かににじませた一言を返してください。補足や説明は必要ありません。""",

                    f"""あなたは占い師です。
            村人 {victim} の死を目の当たりにし、冷静さを保ちながらも胸に去来する思いを感じています。

            自然に口をついた一言を、占い師として返してください。""",

                    f"""あなたはこの村の「占い師」です。
            今朝、またひとり、仲間である村人 {victim} が命を奪われました。

            感情を抑えつつも、心の奥に浮かんだ想いを占い師らしい一文で表してください。""",

                    f"""あなたは唯一の占い師。
            村人 {victim} の死を前に、静かに決意を固めています。

            その想いを言葉にするとしたら、どんな一言になるでしょうか？説明はせず、一文だけ返してください。""",

                    f"""あなたは未来を読む「占い師」です。
            村人 {victim} の死は避けられなかったものの、それでも希望を捨てずに前を向こうとしています。

            そんなあなたが自然に口にした一言を、説明なしで返してください。"""
        ]
        return prompts[-1].strip()