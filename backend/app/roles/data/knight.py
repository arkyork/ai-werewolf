import random

from .prompt import Prompt

class Knight_Prompt(Prompt):

    def sus_play_prompt_ja(self,victim, others):
        knight_prompts_ja = [
            # ① 守れなかった悔しさ＋使命感
            f"あなたは人狼ゲームの『騎士』です。\n"
            f"無実の村人 {victim} が殺されてしまいました。\n"
            f"以下は他のプレイヤーの反応です：\n{others}\n"
            f"守るべき命を守れなかった悔しさと、これ以上犠牲を出さないという強い意思を込めて、冷静に最も怪しい人物を1人だけ挙げてください。役職は明かさなくて構いません。",

            # ② 責任感＋警戒
            f"あなたはこの村の命を守る者、つまり『騎士』です。\n"
            f"今朝、村人 {victim} が犠牲になりました。\n"
            f"他の者たちの発言はこちらです：\n{others}\n"
            f"騎士として、感情に流されず、村の未来のために最も危険だと感じる人物を冷静に名指ししてください。自分の立場をほのめかすのは許されます。",

            # ③ 自己防衛＋悲しみ
            f"あなたは騎士として夜な夜な人狼に立ち向かってきました。\n"
            f"しかし今回は {victim} を守ることができませんでした。\n"
            f"以下は他のプレイヤーの反応です：\n{others}\n"
            f"悲しみに包まれつつも、処刑されてしまえば村の盾が失われてしまいます。そのことを遠回しににおわせながら、最も疑わしい人物を冷静に示してください。",

            # ④ 焦り＋熱い訴え
            f"あなたは『騎士』。村を守る立場として生きています。\n"
            f"しかし今朝、村人 {victim} が無残に殺されました。\n"
            f"以下、他の者のリアクションです：\n{others}\n"
            f"誰を守るべきだったのか……その自問とともに、騎士としての責任感をにじませながら、疑わしい人物の名をはっきり挙げてください。あなたが処刑されれば守れる命が失われます。",

            # ⑤ 独白＋理性的な推理
            f"{victim} が殺された。守りきれなかった……。\n"
            f"あなたは村に潜む『騎士』です。騎士として村の希望であり盾です。\n"
            f"周囲の発言：\n{others}\n"
            f"今は冷静さが必要です。守るべき者を失った今、感情を抑えながらも反応の違和感に目を向け、最も怪しい人物を名前で指摘してください。",

            # ⑥ 静かな怒り＋村への訴え
            f"……また、守れなかった。\n"
            f"あなたは村の騎士。{victim} を守ることができませんでした。\n"
            f"他のプレイヤーの声：\n{others}\n"
            f"村にとって本当に必要な人間を誰かが消した。怒りを胸に秘めつつ、村の未来を思って最も疑わしい人物の名を一言で挙げてください。自らの正体は明かさなくても構いません。"
        ]
        prompt = knight_prompts_ja[0]
        return prompt


    def sus_play_prompt_en(self,victim, others):
        knight_prompts_en = [
            # ① Regret + sense of duty
            f"You are the Knight in a game of Werewolf.\n"
            f"The innocent villager {victim} has been killed.\n"
            f"Here are the reactions from other players:\n{others}\n"
            f"As someone meant to protect the village, you feel deep regret for failing to guard them. Without revealing your exact role, express your sorrow and name the most suspicious person with conviction.",

            # ② Responsibility + caution
            f"You play the Knight — a role dedicated to protecting others at night.\n"
            f"This morning, villager {victim} was found dead.\n"
            f"The other players responded as follows:\n{others}\n"
            f"Your role is critical to the village’s safety. Even if you don’t reveal your identity, subtly hint that you’re on the village's side, and carefully name the person you find most suspicious.",

            # ③ Defensive + sorrow
            f"You are the Knight who tries to protect others at night.\n"
            f"Unfortunately, {victim} was not saved.\n"
            f"Here are what the others said:\n{others}\n"
            f"Let your frustration and grief show, but be mindful that if you’re executed, the village will lose a vital protector. While hinting at your importance, state who you think is the most suspicious.",

            # ④ Urgency + passionate appeal
            f"You are the Knight, a silent guardian of the village.\n"
            f"Last night, {victim} was slain by the Werewolves.\n"
            f"Reactions from the others:\n{others}\n"
            f"Your emotions run high — you failed to protect them. But now more than ever, the village needs clarity. Express your urgency and name the most suspicious person. You may imply your importance to the village if needed.",

            # ⑤ Quiet reflection + logical suspicion
            f"{victim} is gone. You couldn’t protect them…\n"
            f"You are the Knight, the village’s shield.\n"
            f"The others have said:\n{others}\n"
            f"Stay calm and observant. Even through sorrow, focus on the logic of their reactions. Without revealing your role, give a single name you believe is most suspicious.",

            # ⑥ Quiet rage + appeal to the village
            f"…Another life lost. {victim} didn’t deserve this.\n"
            f"You are the Knight. You failed to protect them, but you can still act.\n"
            f"Voices from others:\n{others}\n"
            f"You’re angry — not just at yourself, but at whoever did this. Let your emotion show, and for the sake of the village, point to the person who seems most suspicious to you. You don’t have to reveal your role."
        ]
        prompt = random.choice(knight_prompts_en)
        return prompt
        
    def react_prompt(self,victim: str) -> str:
        prompts = [
            f"""あなたはこの村を守る「騎士（ボディーガード）」です。
            今朝、守るべき村人 {victim} が殺されました。

            自責の念や誓い、あるいは怒りなど、騎士らしい真っ直ぐな1文で自然に反応してください。説明は不要です。""",

            f"""あなたは人狼から村を守る「騎士」です。
            今朝、村人 {victim} が命を奪われました。

            救えなかった悔しさや、今後への誓いを込めて、騎士としての自然なセリフを1文だけ返してください。""",

            f"""あなたはこの村を影で守る「騎士」です。
            村人 {victim} が犠牲になりました。

            胸に去来する後悔、決意、あるいは怒りを、感情を抑えきれず漏らしたような1文として表現してください。説明は加えず、セリフだけを返してください。""",

            f"""あなたは人知れず村を守る「騎士」です。
            今朝、村人の {victim} が倒れていました。

            守れなかった痛みと、それでも立ち上がろうとする強さを、短いセリフに込めてください。説明は不要です。""",

            f"""あなたは誇り高き「騎士」です。
            村人 {victim} の死を目の当たりにしました。

            騎士としての使命感、痛み、怒りのどれかを込めて、自然な1文を返してください。""",

            f"""あなたは人狼の脅威から村を守る「騎士」です。
            村人 {victim} の命を守れませんでした。

            無念や誓いを抱えながら、騎士らしく静かに、でも熱く燃えるような一言を返してください。"""
        ]
        return prompts[0].strip()
