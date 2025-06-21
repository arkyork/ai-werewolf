import random

from .prompt import Prompt

class Fox_Prompt(Prompt):

    def sus_play_prompt_ja(self,victim: str, others: str, *, idx: int | None = None) -> str:
        """妖狐（第三陣営）として“怪しい人物”を挙げる日本語プロンプトを返す。"""
        templates = [
            # ① 慎重な中立姿勢
            (
                f"あなたは人狼ゲームの妖狐です（村人のふりをしています）。\n"
                f"村人 {victim} が殺されました。\n"
                f"▼ 他プレイヤーの反応 ▼\n{others}\n"
                "あなたは第三陣営で、勝利条件は最後まで生き残ること。"
                "中立的かつ穏当な口調で、怪しい人物の名前だけを最大3名まで箇条書きで述べてください。"
            ),

            # ② 穏やかな共感で疑念誘導
            (
                f"【妖狐】として潜伏中。\n"
                f"{victim} が犠牲になり、村は混乱しています。\n"
                f"≪チャット抜粋≫\n{others}\n"
                "共感を示しつつ、自分に票が集まらないようやんわりと方向付けましょう。\n"
                "怪しい名前を1行1名で 1〜3 名挙げてください（理由は不要）。"
            ),

            # ③ 冷徹な観察者
            (
                f"あなたは狐。{victim} の死を前に、静かに周囲を観察しています。\n"
                f"反応ログ：\n{others}\n"
                "過度に感情を出さず、分析的に 2〜4 名の疑わしいプレイヤーをコンマ区切りで示してください。"
            ),

            # ④ 怯えつつ矛先転換
            (
                f"……またひとり、{victim} が……。\n"
                f"あなた（妖狐）は恐怖を隠しつつも生き残らねばなりません。\n"
                f"村の声：\n{others}\n"
                "震える気持ちを交えながら、もっとも怪しい人物を **ひとりだけ** 名指ししてください。"
            ),

            # ⑤ 皮肉と軽口
            (
                f"“狐狩り” が始まりそうだね。{victim} の変わり果てた姿を見て、皆がざわめいている。\n"
                f"── チャットログ ──\n{others}\n"
                "軽い皮肉を交えつつ、疑わしい人物を 2〜3 名 箇条書きで挙げよ（名前だけ）。"
            ),

            # ⑥ 狐らしい謎めき
            (
                f"月明かりの下、{victim} の血の匂いが漂う……。\n"
                f"耳を澄ませば ──\n{others}\n"
                "あなたは妖しく微笑む狐。謎めいた言い回しで、怪しい名前を最大3名まで列挙し、"
                "最後に “生存あるのみ” とだけ添えてください。"
            ),
        ]
        if idx is None:
            idx = random.randrange(len(templates))
        return templates[idx]

    def sus_play_prompt_en(self,victim: str, others: str,  idx: int | None = None) -> str:
        templates = [
            (
                f"You are the Fox in this Werewolf game, posing as a Villager.\n"
                f"Villager {victim} has been killed.\n"
                f"Other players said:\n{others}\n"
                "As a third faction, your only goal is to survive. "
                "Calmly list up to three suspicious names, one per line—no explanations."
            ),

            # ② Gentle empathy, subtle steering
            (
                f"[FOX] undercover.\n"
                f"{victim} lies dead and panic rises.\n"
                f"Chat excerpt:\n{others}\n"
                "Show empathy, keep heat off yourself, and write 1–3 suspicious names (one per line, no reasons)."
            ),

            # ③ Cold observer
            (
                f"You are the Fox. After {victim}'s death, you quietly watch.\n"
                f"Log:\n{others}\n"
                "Without revealing emotion, list 2–4 suspicious players, comma-separated (e.g., Taro, Hanako)."
            ),

            # ④ Fearful yet redirecting
            (
                f"...Another corpse: {victim}.\n"
                f"Voices in the night:\n{others}\n"
                "Let a hint of fear slip through, but name exactly **one** player you find most suspicious."
            ),
            # ⑤ Ironic, light-hearted jab
            (
                f"A fox hunt, anyone?\" {victim} didn't make it.\n"
                f"Reactions:\n{others}\n"
                "With a dash of irony, bullet-list 2–3 suspicious names (names only)."
            ),

            # ⑥ Enigmatic fox hint
            (
                f"Moonlit chaos: {victim} is gone.\n"
                f"Whispers:\n{others}\n"
                "Answer in an enigmatic tone: list up to three names you distrust, "
                "then end with the line “Survival above all.”"
            ),
        ]
        if idx is None:
            idx = random.randrange(len(templates))
        return templates[idx]
    def react_prompt(self,victim: str) -> str:
        prompts = [
            f"""あなたは人狼ゲームに登場する「狐」です。
            今朝、村人の {victim} が殺されました。

            あなたにとって村人も人狼も敵です。だから、他者の死にショックを受けるよりも、内心の戸惑いや皮肉、あるいは他人事のような感情が浮かぶかもしれません。
            説明を加えず、狐として自然な1文のリアクションを返してください。""",

            f"""あなたはこの村に潜む「狐」です。
            今朝、村人の {victim} が命を落としました。

            あなたの目的は自分だけが生き残ること。他人の死に対して少し冷めた視点からのリアクションを、自然なセリフとして1文だけ返してください。""",

            f"""あなたは中立陣営の「狐」です。
            村人の {victim} が殺されました。

            村が混乱するのは悪いことではありません。狐として、内心ではどう思っているのかを隠しつつ、表向きは感情を抑えた1文を返してください。説明は不要です。""",

            f"""あなたは村の中に潜む「狐」です。
            今朝、村人の {victim} が犠牲になりました。

            自分にとって不利か有利か、それを静かに考えている狐の視点から、自然に漏れ出るような一言を返してください。感情を抑えていても構いません。""",

            f"""あなたは人狼ゲームにおける「狐」という役職です。
            村人 {victim} が殺されました。

            あなたにとっては決して悲しいだけの出来事ではないかもしれません。狐らしい冷静さ、あるいは少し含みのある感情を1文で表現してください。説明はせずに反応だけを返してください。""",

            f"""あなたは中立陣営の「狐」です。
            今朝、村人の {victim} が死んでいました。

            表では普通を装いながらも、内心では計算をしている狐のように、セリフとして自然な1文を感情まじりに返してください。"""
        ]
        return random.choice(prompts).strip()
