
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login


model = AutoModelForCausalLM.from_pretrained("./llama-3-8b-elyza-ja-werewolf-awq")
tokenizer = AutoTokenizer.from_pretrained("./llama-3-8b-elyza-ja-werewolf-awq")

print("読み込み完了")


model.push_to_hub("")
tokenizer.push_to_hub("")