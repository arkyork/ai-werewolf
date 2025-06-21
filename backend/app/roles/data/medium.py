import random

from .prompt import Prompt

class Medium_Prompt(Prompt):

    def sus_play_prompt_ja(self,victim, others):
        medium_prompts_ja = [
            # ① 村人側であることの暗示＋感情的な疑い
            f"あなたは人狼ゲームの霊媒師です。\n"
            f"村人である {victim} が殺されました。\n"
            f"以下は他のプレイヤーの反応です：\n{others}\n"
            f"村人側として、このまま処刑されてしまっては村の勝利が遠のいてしまいます。\n"
            f"役職を明かす必要はありませんが、村人陣営であることをにじませながら、感情的に一番怪しい人物を名前で1人挙げてください。",

            # ② 死者の無念＋自己防衛を含む疑い
            f"あなたは霊媒師。{victim} の無念が心に響きます。\n"
            f"こちらが他のプレイヤーの反応です：\n{others}\n"
            f"あなたが処刑されれば、死者の真実を伝える手段は失われます。\n"
            f"自分の正体を明言せずとも村の役に立つ存在であることを示しつつ、感情を交えて最も怪しい人物を1人挙げてください。",

            # ③ 混乱の中での警戒と決断
            f"村人 {victim} が殺され、村には恐怖と混乱が広がっています。\n"
            f"あなたは霊媒師です。以下のリアクションを読んでください：\n{others}\n"
            f"冷静に見える者、感情的な者、沈黙している者──その中で最も不自然だと感じた人物を、感情を交えつつもはっきりと名指ししてください。\n"
            f"村人側の存在として、自分が処刑されないように意識するのも重要です。",

            # ④ 村の未来のための冷静な推理
            f"あなたは霊媒師。\n"
            f"{victim} の死を前に、村には悲しみが漂っています。\n"
            f"以下は他プレイヤーの発言です：\n{others}\n"
            f"あなたが処刑されてしまえば、死者から得られる情報が途絶えてしまいます。\n"
            f"役職を明かさずとも「村を導ける存在」であることをにおわせながら、最も怪しい人物を1人だけ挙げてください。",

            # ⑤ 自己防衛＋感情を込めた訴え
            f"{victim} が殺されました。\n"
            f"あなたは霊媒師として、死者の思いを汲み、村を守ろうとしています。\n"
            f"他のプレイヤーの反応：\n{others}\n"
            f"あなた自身が処刑されれば村にとって不利になります。\n"
            f"「自分には村にとって意味のある役割がある」と暗に伝えながら、心の揺れを込めて疑わしい人物を1人名指ししてください。",

            # ⑥ 静かな怒り＋村への訴え
            f"あなたは霊媒師。\n"
            f"{victim} の死に、怒りと悲しみが胸にこみ上げてきます。\n"
            f"以下は村の者たちの反応です：\n{others}\n"
            f"自分の立場は明かさずとも、村にとって必要な存在であることを言外に伝えてください。\n"
            f"そして今最も疑わしいと感じた人物を、名前で1人挙げてください。"
        ]
        prompt = random.choice(medium_prompts_ja)
        return prompt

    def sus_play_prompt_en(self,victim, others):
        medium_prompts_en = [
            # ① Hinting at being a Villager + emotional suspicion
            f"You are the Medium in a game of Werewolf.\n"
            f"A Villager named {victim} was killed.\n"
            f"Here are the reactions from the other players:\n{others}\n"
            f"If you're executed, it will be a serious loss for the Village side.\n"
            f"You don’t have to reveal your role, but it’s okay to subtly imply you’re on the Village side.\n"
            f"Please state, with emotion, who you find most suspicious. Name just one player.",

            # ② Carrying the dead’s regret + mild self-defense
            f"You are the Medium. The death of {victim} weighs heavily on your heart.\n"
            f"Below are the reactions from the others:\n{others}\n"
            f"If you are executed, the Village will lose the ability to learn the truth from the dead.\n"
            f"Without stating your role directly, hint that you are a helpful Villager and name the person you find most suspicious.",

            # ③ Confusion in the village + emotional naming
            f"A Villager named {victim} has been killed, and chaos is spreading in the village.\n"
            f"You are the Medium. The following are other players’ responses:\n{others}\n"
            f"Among them, who seemed too calm, too loud, or too quiet?\n"
            f"With both logic and emotion, point to the person you found most suspicious. Don’t forget to protect yourself as someone valuable to the village.",

            # ④ Rational reasoning for the village’s future
            f"You are the Medium.\n"
            f"The death of {victim} brings sorrow to the village.\n"
            f"Here are the reactions from the others:\n{others}\n"
            f"If you are eliminated, the village will lose a valuable perspective.\n"
            f"Even without disclosing your role, subtly show your importance and clearly name the person you find most suspicious.",

            # ⑤ Self-defense + heartfelt appeal
            f"{victim} has been killed.\n"
            f"You are the Medium, trying to protect the village by learning the truth from the dead.\n"
            f"Other players said the following:\n{others}\n"
            f"If you are executed, the village loses a vital ability.\n"
            f"Imply that you have an important role, and from your heart, name one person you find most suspicious.",

            # ⑥ Quiet anger + an appeal to the village
            f"You are the Medium.\n"
            f"The death of {victim} fills you with sorrow and anger.\n"
            f"Here are the other players’ reactions:\n{others}\n"
            f"Don’t reveal your role directly, but let them feel that you are someone the village needs.\n"
            f"Then calmly name the one person you find most suspicious."
        ]
        prompt = random.choice(medium_prompts_en)
        return prompt
    
    def react_prompt(self,victim: str) -> str:
        prompts = [
            f"""あなたは死者の声を聞く「霊媒師」です。
            今朝、村人 {victim} が殺されました。

            死者の無念や悲しみを感じ取りながら、胸に浮かんだ自然な一言を返してください。説明は不要です。""",

                    f"""あなたは村に潜む霊媒師です。
            今朝、村人 {victim} が命を奪われました。

            彼の死に感じた想いや怒りを、静かな感情として1文で表現してください。説明や状況の補足は不要です。""",

                    f"""あなたは霊媒師として、この村の死者と向き合ってきました。
            今朝、またひとり、村人 {victim} が倒れました。

            死者から伝わる感情や、自分の役目への想いをこめた自然なセリフを、1文だけ返してください。""",

                    f"""あなたは死者と語る「霊媒師」です。
            村人 {victim} の命が奪われました。

            その死がもたらす重みと、霊媒師としての責任を静かに受け止める1文を返してください。説明は要りません。""",

                    f"""あなたは人知れず死者の声を伝える「霊媒師」です。
            今朝、村人 {victim} が犠牲になりました。

            誰にも見えない悲しみや、胸の奥で燃える使命感を込めて、自然に漏れたような短いセリフを1つだけ返してください。""",

                    f"""あなたはこの村の「霊媒師」です。
            今朝、またひとり村人 {victim} が命を落としました。

            霊媒師としてその死を重く受け止め、静かに語るような一言を返してください。"""
        ]
        return random.choice(prompts).strip()