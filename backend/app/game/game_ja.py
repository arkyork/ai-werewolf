from vllm import LLM, SamplingParams
import torch

llm = LLM(model="elyza/Llama-3-ELYZA-JP-8B-AWQ")

victim ="gemma"
# サンプルプロンプト
prompts = [
     (
        "以下は人狼ゲームで村人が殺されたときの、他の村人の反応の例です。\n"
        "えっ！？なんであの人が……！僕じゃないよ、信じて！\n"
        "こ、怖い……ち、違うってば……！私じゃないから……！\n"
        f"{victim} が殺された直後の村人としての反応を、1文で出力してください。\n"
    ),
    (
        "以下は人狼ゲームで村人が殺されたときの、他の村人の反応の例です。\n"
        "えっ！？なんであの人が……！僕じゃないよ、信じて！\n"
        "こ、怖い……ち、違うってば……！私じゃないから……！\n"
        f"{victim} が殺された直後の村人としての反応を、1文で出力してください。\n"
    ),
    (
        "以下は人狼ゲームで村人が殺されたときに、潜伏中の人狼が村人のふりをして取り乱した発言の例です。\n"
        "ま、まさか……そんな……次は僕なの……！？\n"
        "嘘だろ……誰がこんなことを……！？（震え声）\n"
        f"{victim} が殺された直後の人狼としての反応を、1文で出力してください。\n"
    )
]

sampling_params = SamplingParams(do_sample=True,temperature=0.8, top_p=0.95)

outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"prompt: {prompt!r}, generated_text: {generated_text!r}")

# 現在のインスタンスを破棄
del llm
torch.cuda.empty_cache()