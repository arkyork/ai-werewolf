# check_awq_vllm.py
import os, importlib.util, sys
from transformers import AutoTokenizer
from awq import AutoAWQForCausalLM
from vllm import LLM
llm = LLM(model="./llama-3-8b-elyza-ja-werewolf-awq")  
