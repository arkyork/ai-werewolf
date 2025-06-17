from vllm import LLM, SamplingParams
import torch

import random
from transformers import AutoTokenizer,AutoModelForCausalLM,pipeline
import Levenshtein
from transformers import set_seed
from roles.wolf import Wolf
from roles.villager import Villager

from .game_base import GAME


set_seed(548)



class Wolf_JA(Game):


    def __init__(self):

        self.llm = LLM(model="elyza/Llama-3-ELYZA-JP-8B-AWQ")  
        self.sampling = SamplingParams(temperature=0.8,
                                       top_p=0.95,
                                       max_tokens=120)
        names = [
            "GPT2",
            "llama3",
            "tinyllama",
            "Mistral",
            "DeepSeek",
            "gemma",
        ]
        self.people = {n: {"role": None, "alive": True} for n in names}
        self.day = 0 
        self.history: list[str] = []  # for logging events in order

        self._assign_roles()
        print("人狼：",self._wolves())


    def _assign_roles(self):
        names = list(self.people.keys())
        
        roles = [Wolf()] + [Villager()] * (len(names) - 1)
        
        random.shuffle(roles)
        
        for name, role in zip(names, roles):
            self.people[name]["role"] = role    
    

    def kill(self):
        # Killの準備
        candidates = self._alive()
        werewolf_name  = self._wolves()[0] #人狼
        werewolf_role = self.people[werewolf_name]["role"]

        messages = werewolf_role.role_play_pormpt(candidates)

        # 出力
        target = self.llm.generate(messages, self.sampling)[0].outputs[0].text.strip()

        
        # レーベンシュタイン距離で確実に判定
        target = self.lenven(target)
        
        if self.people[target]["alive"]:
            self.people[target]["alive"] = False
            self._log(f"Night {self.day}: {target} が死亡しました。")
            self.day += 1
        
        # killされた反応
        kill_reactions = self.react_to_death(target)  

        # sus 誰が怪しい

        suspect_reaction = self.susupect(target,kill_reactions)  

        return [target,kill_reactions,suspect_reaction]     
    


    # 誰かが殺された後、生存者たちが自分の潔白を主張する反応

    def react_to_death(self, victim: str):
        alive = self._alive()
        # ★生存者分まとめてバッチ生成
        prompts = [self.people[n]["role"].react_prompt(victim) for n in alive]
        results = self.llm.generate(prompts, self.sampling)

        # save reactions by dictionary
        all_reactions = {name:"" for name in alive}
        for name, res in zip(alive, results):
            line = res.outputs[0].text.strip()
            
            all_reactions[name] = line

            self._log(f"{name} の反応: 「{line}」")

        return all_reactions

    def susupect(self,victim,kill_reactions):
        alive = self._alive()


        # 生存者分まとめて生成
        prompts = [self.people[n]["role"].sus_prompt(victim,n,kill_reactions) for n in alive]
        results = self.llm.generate(prompts, self.sampling)
        
        # save reactions by dictionary
        all_reactions = {name:"" for name in alive}

        for name, res in zip(alive, results):
            line = res.outputs[0].text.strip()
            
            all_reactions[name] = line

            self._log(f"{name} の反応: 「{line}」")
        
        return all_reactions