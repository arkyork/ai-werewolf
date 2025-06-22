import pandas as pd
from datasets import Dataset
import gc
import shutil
import os
import re
from datasets import load_dataset
from trl import DPOConfig, DPOTrainer
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import (
    LoraConfig, 
    PeftModel, 
    TaskType
)
from transformers.trainer_utils import set_seed
from datasets import load_dataset
import torch
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from huggingface_hub import login
from dotenv import load_dotenv




dfs = []
for i in range(1, 6):
    path = f"./csv/data{i}.csv"
    print(i)
    try:
        df = pd.read_csv(path)
        dfs.append(df)
    except FileNotFoundError:
        dfs.append(f"{path} が見つかりませんでした。")


merged_df = pd.concat(dfs, ignore_index=True)

print(merged_df)

train_dataset = Dataset.from_pandas(merged_df)


def get_prediction(
    prompt: str,
    model: AutoModelForCausalLM,
    tokenizer: AutoTokenizer,
) -> str:
    """プロンプトに対するモデルの応答を取得する"""
    messages = [{"role": "user", "content": prompt}]
    input_ids = tokenizer.apply_chat_template(
        messages, return_tensors="pt", add_generation_prompt=True
    )
    with torch.cuda.amp.autocast():
        generated_ids = model.generate(
            input_ids.to(model.device),
            max_new_tokens=128,
            do_sample=True,

        )
    output_ids = generated_ids[0][input_ids.size(1) :]
    return tokenizer.decode(output_ids)



set_seed(42)


# === 最新の checkpoint-* フォルダを取得 ===
def get_latest_checkpoint(directory):
    checkpoints = [
        d for d in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, d)) and re.match(r"checkpoint-\d+", d)
    ]
    if not checkpoints:
        raise FileNotFoundError("checkpoint-* が見つかりません。")

    # checkpoint-数字 を整数でソート
    latest = max(checkpoints, key=lambda x: int(x.split("-")[1]))
    return os.path.join(directory, latest)

def delete():
    directory = 'final_ckpt'

    # ディレクトリが存在するか確認
    if os.path.exists(directory) and os.path.isdir(directory):
        try:
            shutil.rmtree(directory)
            print(f"'{directory}' ディレクトリを削除しました。")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    else:
        print(f"'{directory}' ディレクトリが存在しません。")






#[5]: tokenizerの設定


base_model_name = "meta-llama/Meta-Llama-3-8B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(base_model_name)

tokenizer.padding_side = "left"

tokenizer.pad_token = tokenizer.eos_token



quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

# モデルの準備
model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    torch_dtype=torch.bfloat16,
    quantization_config=quantization_config,
    device_map="auto",
)

# 参照モデル
ref_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    torch_dtype=torch.bfloat16,
    quantization_config=quantization_config,
    device_map="auto",
)


# LoRAパラメータ
peft_config = LoraConfig(
    r=128,  
    lora_alpha=128, 
    lora_dropout=0.05,  
    task_type=TaskType.CAUSAL_LM,
    target_modules=[
        "q_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
        "k_proj",
        "v_proj",
    ],
)

# 学習パラメータ
dpo_config = DPOConfig(
    output_dir="DPO_results",
    bf16=True, 
    num_train_epochs=6,
    per_device_train_batch_size=4,
    remove_unused_columns=False,
    gradient_accumulation_steps=4,
    gradient_checkpointing=True,
    optim="paged_adamw_8bit",  
    learning_rate=5e-6,
    lr_scheduler_type="cosine",  
    max_grad_norm=0.3,  
    warmup_ratio=0.1,  
    save_steps=50,  
    logging_steps=100,  
    beta=0.1, 
    max_prompt_length=512,  
    max_length=768,  
    report_to="tensorboard", 
    force_use_ref_model=True,

)



# DPOTrainerの準備
trainer = DPOTrainer(
    model=model,
    ref_model=ref_model,
    args=dpo_config,
    train_dataset=train_dataset,
    peft_config=peft_config,
    processing_class=tokenizer,
)


# 学習の実行
trainer.train()

# Trainer内のリソースを手動で解放
if 'trainer' in locals():
    trainer._memory_tracker.stop_and_update_metrics()  # メモリトラッキングを停止
    del trainer  # Trainerオブジェクトを削除


# ガベージコレクタを明示的に呼び出してメモリを解放
gc.collect()

# PyTorchのCUDAキャッシュを解放
torch.cuda.empty_cache()

# IPCを使用した非同期メモリ解放
torch.cuda.ipc_collect()



base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    return_dict=True,
)


dpo_results_dir = "DPO_results"
latest_ckpt_path = get_latest_checkpoint(dpo_results_dir)

## マージ
model = PeftModel.from_pretrained(base_model, latest_ckpt_path)

model = model.merge_and_unload()

#トレーニング後の結果


tokenizer.save_pretrained("Llama-elyza-3-8B-DPO")
model.save_pretrained("Llama-elyza-3-8B-DPO")




