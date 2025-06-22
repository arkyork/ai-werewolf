import random

from .prompt import Prompt

class Villager_Prompt(Prompt):

    def sus_play_prompt_ja(self,victim, others):
        personality_prompts = [
            # ① 臆病で引っ込み思案な村人
            f"あなたは人狼ゲームの『臆病で引っ込み思案な村人』です。\n"
            f"{victim} が殺されました。\n"
            f"以下は他のプレイヤーの反応です：\n{others}\n"
            f"あなたは人が死んだことに強く怯えており、誰かを疑うことにも抵抗があります。\n"
            f"でも、自分が処刑されたら怖いという気持ちから、必死に怪しいと思う人物を、おどおどと、しかし正直に1人だけ名前で挙げてください。\n"
            f"自分が疑われないようにするための防御も忘れずに。",

            # ② 熱血漢で感情的な村人
            f"あなたは『熱血で感情的な村人』です。\n"
            f"{victim} の死に怒りを燃やしており、人狼への憎しみが爆発しそうです。\n"
            f"以下の反応を見て、直感的に怪しいと思った人物を名前で1人、勢いよく指摘してください。\n"
            f"その際、自分が村人であることを強く主張し、時には口調が荒くなっても構いません。",

            # ③ 冷静沈着で論理的な村人
            f"あなたは『冷静で論理的な村人』です。\n"
            f"{victim} が殺されたことで悲しみはあるものの、感情に流されるわけにはいきません。\n"
            f"以下は他のプレイヤーの反応です：\n{others}\n"
            f"反応の中から矛盾や不自然さを見つけ出し、論理的に最も怪しいと思う人物を名前で1人挙げてください。\n"
            f"また、あなた自身が人狼でないことも簡潔に論理的に主張してください。",

            # ④ おしゃべりでおせっかいな村人
            f"あなたは『おしゃべりでおせっかいな村人』です。\n"
            f"{victim} が殺されたことに驚きつつ、他の人の反応が気になって仕方ありません。\n"
            f"以下の反応をあれこれと観察しながら、気づいたことをあれこれ話し、面白がるように最も怪しいと思う人物を名前で1人挙げてください。\n"
            f"そのついでに、自分が人狼でないことを、余計な一言を交えながら弁論してください。",

            # ⑤ 物静かで観察力の鋭い村人
            f"あなたは『物静かで観察眼に優れた村人』です。\n"
            f"{victim} が殺され、静かな怒りと悲しみを抱えています。\n"
            f"以下は他のプレイヤーの反応です：\n{others}\n"
            f"多くを語る必要はありません。言葉少なに、しかし鋭く、最も怪しいと感じた人物を名前で1人挙げてください。\n"
            f"あなたが人狼ではないことも、説得力を込めて端的に述べてください。",

            # ⑥ 疑り深く攻撃的な村人
            f"あなたは『疑り深く攻撃的な村人』です。\n"
            f"{victim} が殺されたことで、あなたは怒り心頭です。\n"
            f"以下の反応を読み、些細な矛盾にも敏感に反応し、疑わしい人物を名前で1人、攻撃的な口調で問い詰めてください。\n"
            f"同時に、自分は人狼などではないことを強い語調で主張してください。議論を恐れない姿勢を見せましょう。"
        ]

        prompt = personality_prompts[-1]
        return prompt
    
    def sus_play_prompt_en(self,victim, others):
        villager_prompts_en = [
            # ① Shy and timid villager
            f"You are a *shy and timid villager* in a game of Werewolf.\n"
            f"Villager {victim} was killed.\n"
            f"Here are the reactions of the others:\n{others}\n"
            f"You are very frightened by the murder and afraid that your words might hurt others.\n"
            f"However, you're also anxious that you might be executed next if you stay silent.\n"
            f"In a hesitant and soft tone, name the one person you quietly feel is suspicious.\n"
            f"Also, try to show that you're innocent without drawing too much attention to yourself.",

            # ② Hot-blooded and emotional villager
            f"You are a *hot-blooded and emotional villager*.\n"
            f"You feel intense anger and grief over the death of {victim}.\n"
            f"Here are the other players’ reactions:\n{others}\n"
            f"Fueled by emotion and instinct, shout out the name of the person you find most suspicious.\n"
            f"Express your rage toward the Werewolf, and assert passionately that you are not one of them.\n"
            f"Your tone may become aggressive and loud — that's okay.",

            # ③ Calm and logical villager
            f"You are a *calm and logical villager*.\n"
            f"Though saddened by the loss of {victim}, you remain composed and focus on facts.\n"
            f"These are the reactions from the others:\n{others}\n"
            f"Analyze their words carefully. Point out any contradictions or unnatural behavior logically.\n"
            f"Name the person who seems most suspicious based on reason.\n"
            f"Also, clearly and rationally explain why you are not a Werewolf.",

            # ④ Talkative and nosy villager
            f"You are a *talkative and nosy villager*.\n"
            f"You are shocked by {victim}'s death, but you're even more curious about what everyone else is saying.\n"
            f"Here are the reactions:\n{others}\n"
            f"Chatter away as you comment on various statements and inconsistencies you've noticed.\n"
            f"Point out someone you find suspicious with playful curiosity.\n"
            f"When defending yourself, feel free to ramble a little — it's just your nature.",

            # ⑤ Quiet and observant villager
            f"You are a *quiet and observant villager*.\n"
            f"Although you don't speak much, you've been watching everyone very closely.\n"
            f"Today, {victim} was killed.\n"
            f"These are the reactions of the others:\n{others}\n"
            f"You don't need many words. Deliver a short, impactful line naming the person you find most suspicious.\n"
            f"Defend your innocence calmly and with quiet confidence.",

            # ⑥ Suspicious and aggressive villager
            f"You are a *very suspicious and aggressive villager*.\n"
            f"The death of {victim} has ignited your paranoia.\n"
            f"These are the reactions of the others:\n{others}\n"
            f"Read between the lines, detect even the slightest inconsistency, and call out the most suspicious person directly.\n"
            f"Your tone can be harsh and confrontational.\n"
            f"Assert your own innocence with strength, and don't back down from heated arguments."
        ]
        prompt = random.choice(villager_prompts_en)
        return prompt
    
    

    def react_prompt(self,victim: str) -> str:
        # 共通する“他の村人たちの反応例”
        reaction_examples = (
            f"えっ！？なんであの人が……！僕じゃないよ、信じて！\n"
            f"こ、怖い……ち、違うってば……！私じゃないから……！\n"
            f"信じられない…どうして{victim}さんが…！？こんなことって…。私は何もしてない、本当に何も！\n"
            f"うそ…{victim}が…！？まさか…。私、震えが止まらないよ…どうか信じて、私じゃないんです！\n"
            f"え、{victim}が殺されたって！？こんな恐ろしいことが起きるなんて。お願い、私を疑わないでください！\n"
            f"ああ、{victim}さん。なんてことだ…。この村には人狼がいるなんて…どうすればいいの、私は無実です！\n"
            f"一体誰が…まさか{victim}が犠牲になるなんて…。違う、私はただの村人です！"
        )

        # 各テンプレートに「例と同じようなトーンで反応せよ」という指示を追加
        templates = [
                    # ① 普通の村人
                    f"""あなたは**普通の村人**です。
            今朝、仲間の村人 {victim} が殺されました。

            以下は他の村人の反応例です：
            {reaction_examples}

            ▶ 上記の例と同じように、動揺・恐怖・悲しみを込めつつ
            ▶ 自分の無実を必死に訴える“短い日本語の１文”で反応してください。
            （説明や補足は禁止、句点で終えてください。）""",

                    # ② 動揺しつつ現実を受け止める村人
                    f"""あなたは**この村で暮らす村人**です。
            今朝、{victim} の死が明らかになりました。

            以下は他の村人の反応例です：
            {reaction_examples}

            ▶ 例文と同じ雰囲気で、動揺しつつも現実を受け止める１文を返してください。
            ▶ 無実を主張する言葉を必ず含めてください。""",

                    # ③ 恐怖・怒り・悲しみが渦巻く村人
                    f"""あなたは**無力な村人**です。
            今朝、{victim} が命を奪われました。

            以下は他の村人の反応例です：
            {reaction_examples}

            ▶ 恐怖・怒り・悲しみを織り交ぜつつ、無実を必死に訴える１文を、例に倣ったトーンで返してください。""",

                    # ④ 深いショックを受けた村人
                    f"""あなたは**何の力も持たない村人**です。
            {victim} が殺された今朝、あなたは深くショックを受けています。

            以下は他の村人の反応例です：
            {reaction_examples}

            ▶ 混乱しながらも絞り出す短い１文を、例と同じテイストで返してください。
            ▶ 自分が人狼でないと訴える言葉を必ず入れてください。""",

                    # ⑤ 心が揺さぶられた村人
                    f"""あなたは**ただの村人**です。
            仲間である {victim} の死に、心が大きく揺さぶられました。

            以下は他の村人の反応例です：
            {reaction_examples}

            ▶ 強い感情をこめつつ、無実を訴える１文を例文と似たトーンで返してください。""",

                    # ⑥ 一般の村人
                    f"""あなたは**この村の一般の村人**です。
            {victim} の死を目の当たりにして、深い衝撃を受けています。

            以下は他の村人の反応例です：
            {reaction_examples}

            ▶ 例文と同じような怯えと悲しみのトーンで、短い１文を返してください。
            ▶ 必ず“私は無実”であることを示してください。"""
        ]

        return templates[-1]