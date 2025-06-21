import random

from .prompt import Prompt

class Baker_Prompt(Prompt):

    def sus_play_prompt_ja(self,victim,others):

        # -----------------------------
        # 日本語テンプレート（6パターン）
        # -----------------------------
        baker_prompts_ja = [
            # ① しっとり悲嘆＋警戒
            f"あなたは人狼ゲームのパン屋です。\n"
            f"親しい村人 {victim} が無残にも殺されました。\n"
            f"以下は他のプレイヤーの反応です：\n{others}\n"
            f"パン屋が処刑されれば、朝食の香りも希望も失われてしまいます。役職名を明かさずとも『村を支える立場』であることをほのめかしながら、胸に去来する感情を交えつつ、誰が怪しいのか率直に語ってください。",

            # ② 焦り＋訴えかけ
            f"ここは人狼に脅かされる小さな村。あなたは唯一のパン屋です。\n"
            f"今夜、無実の村人 {victim} が倒れました。\n"
            f"他の者たちの反応：\n{others}\n"
            f"『自分を吊るのは村の損失だ』と遠回しに示唆しつつ、心の動揺とともに最も疑わしい人物を指摘してください。",

            # ③ 冷静分析＋わずかな感情
            f"あなたは村のパン屋。朝のパンを失えば皆が弱ることを誰より知っています。\n"
            f"村人 {victim} が殺害され、周囲は騒然。\n"
            f"以下、プレイヤーたちの第一声です：\n{others}\n"
            f"冷静に反応を観察しながらも、自身が処刑対象にならないよう匂わせつつ、感情を込めて『怪しい人物』を名前で挙げてください。",

            # ④ 強めの悲痛＋自己防衛
            f"あなたはパン屋です。今朝の犠牲者は {victim} —— また仲間が減りました。\n"
            f"周囲の発言は以下の通り：\n{others}\n"
            f"パン屋を失えば村の士気は崩壊します。役職を明言せずとも“村に不可欠な存在”であるとほのめかし、怒りと悲しみを交えながら最も怪しい者を叫ぶように示してください。",

            # ⑤ 祈り＋共感訴求
            f"パンの香りで村を守るあなた（パン屋）ですが、{victim} が無残に散りました。\n"
            f"他のプレイヤーのリアクション：\n{others}\n"
            f"『私まで失えば朝の温もりが消える』ことを遠回しに感じさせつつ、共感的に語りながら怪しい人物を一人だけ挙げてください。",

            # ⑥ 疑心暗鬼の独白調
            f"……また犠牲者だ。{victim} まで……。\n"
            f"あなたはパン屋。村の腹と心を満たす最後の砦です。\n"
            f"皆の声：\n{others}\n"
            f"処刑されれば村は飢えと絶望に沈みます。役職を直接口にせず、胸の不安を吐露しつつ、特に怪しむ人物を感情的に名指ししてください。"
        ]
        prompt = random.choice(baker_prompts_ja)
        return prompt

    
    def sus_play_prompt_en(self,victim,others):
        # -----------------------------
        # English templates (6 patterns)
        # -----------------------------
        prompts = [
            # ① Subdued grief + watchfulness
            f"You are the village Baker in the Werewolf game.\n"
            f"Beloved villager {victim} has been slain.\n"
            f"Here are the other players' reactions:\n{others}\n"
            f"If the Baker is executed, the village loses both bread and hope. Without stating your exact role, gently hint that you hold a vital villager position, then—mixing your feelings—call out the player you find most suspicious.",

            # ② Alarmed plea
            f"Darkness has fallen on the village, and you—the only Baker—stand shaken.\n"
            f"Villager {victim} was murdered tonight.\n"
            f"Reactions from the others:\n{others}\n"
            f"Imply that lynching you would cripple the villagers, then passionately point to the person you suspect the most.",

            # ③ Calm analysis + slight emotion
            f"As the Baker you know how fragile morale is without fresh bread.\n"
            f"{victim} is gone, and whispers swirl.\n"
            f"Players spoke as follows:\n{others}\n"
            f"Remain composed, hint at your importance to the village, and—with a touch of emotion—name the single player who seems most suspicious.",

            # ④ Strong anguish + self-defense
            f"You are the Baker. Another innocent—{victim}—has fallen.\n"
            f"The others reacted like this:\n{others}\n"
            f"Make it clear (without outright saying so) that losing you would doom the village, blend anger and sorrow, and emotionally shout out who you believe is the werewolf.",

            # ⑤ Prayerful tone + empathy
            f"The scent of bread is all that steadies this town, yet {victim} lies dead.\n"
            f"Here are everyone’s first words:\n{others}\n"
            f"Humbly suggest your indispensability while speaking with empathy, then single out the player whose reaction worries you most.",

            # ⑥ Paranoid monologue
            f"…Another body. {victim}. Why?\n"
            f"You, the Baker, keep the village fed—and sane.\n"
            f"Voices ring out:\n{others}\n"
            f"If they hang you, hunger and despair will reign. Without naming your role, pour out your fears and emotionally accuse the one you distrust the most."
        ]
        return random.choice(prompts).strip()
    
    def react_prompt(self,victim: str) -> str:
        prompts = [
            f"""あなたは人狼ゲームに登場する「パン屋」です。
            仲間の村人である {victim} が殺されました。

            現実の人間のように、ショックと深い悲しみをこめて自然な1文で反応してください。
            友人を失ったパン屋として、説明や役職名を入れずに、感情的な一言を返してください。
            """,

            f"""あなたは村の「パン屋」です。
            大切な村人仲間の {victim} が今朝、殺されました。

            混乱や信じられない気持ち、悲しみ、怒りなどを含めたリアルな感情のこもった1文を返してください。
            セリフのように自然に、友人の死に対する心からのリアクションを出力してください。
            """,

            f"""あなたは人狼ゲームの中でパン屋を演じています。
            信頼していた村人 {victim} が人狼に襲われて亡くなりました。

            友達を失った現実の人間として、説明をせず、感情のこもった1文のリアクションを出力してください。
            涙が出そうになるような、率直な反応で構いません。
            """,

            f"""あなたは毎朝パンを焼くパン屋です。
            村の仲間 {victim} が殺されました。

            その喪失に対する率直な1文を、説明抜きで感情だけで表現してください。
            「パン屋として友達を失ったショック」が伝わる自然なセリフを書いてください。
            """,
            f"""あなたはこの村の「パン屋」という役割で人狼ゲームに参加しています。
            今朝、親しい友人である {victim} が無惨にも殺されました。

            悲しみや喪失感を込めて、まるで本当に友人を失ったかのような自然な1文を出力してください。
            説明や状況は不要です。感情のあふれる一言だけを返してください。
            """,

            f"""あなたは人狼ゲームにおけるパン屋です。
            昨夜、仲間の村人 {victim} が命を奪われてしまいました。

            その現実に打ちのめされるような感情を込めて、説明をせず自然な一文のリアクションをしてください。
            感情的に取り乱していても構いません。
            """
        ]
        return random.choice(prompts).strip()