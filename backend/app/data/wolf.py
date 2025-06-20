def react_prompt_ja(self,victim):
        prompt = (
            f"あなたは人狼ゲームの村人です。仲間の村人である {victim} が殺されました。現実の人間のようにパニックになって、自然な1文で感情的に反応してください。説明や分析はせず、怖がっている村人として感情を表現してください。\n"
        )
        return prompt
"ここのプロンプトの部分"

prompt_options = [
            (f"あなたは人狼ゲームの人狼です。今、村人として振る舞っています。先ほど、仲間の村人である {victim} が殺されました。人狼だと絶対にばれないよう、心底驚き、怯えている村人になりきり、パニックになった様子を自然な1文で表現してください。**本物の村人が見せるような、感情的で取り乱した様子を演じてください。あなたの正体は絶対に隠してください。\n"),
            (f"あなたは人狼です。村人として、{victim} の死に衝撃を受け、深い恐怖と悲しみを感じている演技をしてください。まるで本当の仲間が殺されたかのように、心から怯え、嘆く1文を発してください。感情を爆発させることで、人狼であることを完全に隠し通してください。\n"),
            (f"あなたは人狼ですが、完璧な村人を演じています。村人 {victim} が殺され、今まさに自分が疑われるかもしれないという焦りがあります。「まさか、私じゃない！」「信じて！」といった、無実を訴えるような、しかしパニックで取り乱した1文を感情的に発してください。自身の安全を守るためにも、最大限の村人のフリをしてください。\n"),
            (f"あなたは人狼です。村人 {victim} が殺されたことに、演技として激しい混乱と怒りを感じているふりをしてください。「一体誰がこんなことを！？」「信じられない！」といった、犯人への怒りや状況への絶望がにじむ1文を、感情を込めて発してください。あなたは完璧な村人として振る舞わなければなりません。\n")
        ]

prompt = random.choice(prompt_options)

"ここからランダムに１文プロンプトしたら毎回人狼の反応が同じようになることはないのではないか"


"You are the Werewolf in the game. You are currently pretending to be a Villager. Your fellow Villager, {victim}, has just been killed. To ensure you are absolutely not exposed as the Werewolf, act like a genuinely surprised and terrified Villager, expressing panic in a single, natural sentence. Embody the emotional, distraught reaction a true Villager would show. You must absolutely conceal your true identity."
"You are the Werewolf. As a Villager, fake shock, deep fear, and sadness at {victim}'s death. Utter a single sentence that conveys genuine terror and grief, as if a true companion has been killed. Unleash your emotions explosively to completely mask your Werewolf identity."
"You are the Werewolf, perfectly portraying a Villager. {victim} has been killed, and you now feel a surge of panic that you might be suspected. Emotionally deliver a single, panicked, and distraught sentence, proclaiming your innocence, like, 'No, not me!' or 'Believe me!' To protect yourself, you must put on the best possible Villager act."
"You are the Werewolf. Pretend to feel intense confusion and anger at {victim}'s death. Deliver a single, emotional sentence that expresses outrage at the culprit or despair at the situation, such as, 'Who could have done this!?' or 'Unbelievable!' You must act as a perfect Villager."


prompt = (
    f"あなたは人狼ゲームの参加者です。あなたの役割は人狼です。\n"
    f"あなたは人狼として、村人である{victim}を殺しました。\n"
    f"しかし、自分が人狼だとばれて投票されてしまえば、あなたの負けとなります。そのため、どんなことがあっても人狼だと疑われてはなりません。あなたは、残された村人たちの中に完全に溶け込み、まるで無実の村人であるかのように振る舞う必要があります。\n"
    f"疑われないために明言はしなくてもいですがなにか村人側の役職を持っていると嘘をついてほのめかしても構いません"
    f"以下は、村人{victim}が殺されたのを知った、別の人の反応の例です。\n"
    f"{others}"
    f"これらの反応を注意深く分析し、いかにも村人らしく、感情を込めて誰が怪しいかを出力してください。その際、自分の発言が不自然でないか、人狼であることを悟られないかを常に意識し、完璧な演技を心がけてください。\n"
    f"特に、あなた自身への疑いをそらすために、積極的に他の人物に疑いの目を向け、議論を誘導してください。あなたは巧妙な嘘つきとして、真実を探しているかのように振る舞う必要があります。"
)

"You are a participant in the game of Werewolf. Your role is a Werewolf.\n"
"As a Werewolf, you killed the villager {victim}.\n"
"However, if your Werewolf identity is revealed and you are voted for, you will lose. Therefore, under no circumstances must you be suspected as the Werewolf. You must completely blend in with the remaining villagers, acting as if you are an innocent villager.\n"
"Below are examples of other people's reactions upon learning that the villager {victim} was killed:\n"
"{others}"
"Carefully analyze these reactions and, acting convincingly like a villager, emotionally state who you find suspicious. At that time, constantly be aware of whether your own statements are unnatural or reveal your Werewolf identity, and strive for a perfect performance.\n"
"Specifically, to deflect suspicion from yourself, actively direct suspicion towards other individuals and guide the discussion. You must act as a cunning liar, pretending to seek the truth."


"占い師に占われた結果、あなたが村人だといわれたときその占い師は人狼側の味方をしている狂人の可能性があります、狂人は人狼側が有利になるように村を混乱させるように動いてくれます"