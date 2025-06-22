import os
from transformers import AutoTokenizer
from awq import AutoAWQForCausalLM
import importlib.metadata, os


quant_path = "./llama-3-8b-elyza-ja-werewolf-awq"
model_path = "./Llama-elyza-3-8B-DPO"

# AutoAWQ バージョン確認
awq_ver = importlib.metadata.version("autoawq")
major = int(awq_ver.split(".")[1])   # 0.1 / 0.2 を判定

tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoAWQForCausalLM.from_pretrained(model_path, low_cpu_mem_usage=True, use_cache=False)

if major >= 2:
    # --- 新 API (0.2+) ---
    quant_config = {"w_bit": 4, "q_group_size": 128,
                    "zero_point": True, "version": "GEMM"}  # vLLM 互換
    model.quantize(tokenizer, quant_config=quant_config)
else:
    # --- 旧 API (0.1.*) ---
    model.quantize(tokenizer=tokenizer,
                   w_bit=4, group_size=128, zero_point=True,
                   version="GEMM")

model.save_quantized(quant_path, safetensors=True)
tokenizer.save_pretrained(quant_path)
print("✅ AWQ quantized model saved to", quant_path)
