from vllm import LLM, SamplingParams
import torch

import random
from transformers import AutoTokenizer
import Levenshtein
from transformers import set_seed
from roles.wolf import Wolf
from roles.villager import Villager
from roles.seer import Seer
from roles.madman import Madman

from .game_base import Game

class Wolf_JA(Game):

    def __init__(self):

        self.llm = LLM(model="elyza/Llama-3-ELYZA-JP-8B-AWQ")  
        self.sampling = SamplingParams(temperature=0.8,
                                       top_p=0.95,
                                       max_tokens=120)
        self.tokenizer = AutoTokenizer.from_pretrained("elyza/Llama-3-ELYZA-JP-8B-AWQ")
        names = [
            "llama-3.1",
            "Llama-3.2",
            "llama3",
            "tinyllama",
            "Mistral",
            "DeepSeek",
            "gemma",
            "Phi-4",
        ]
        self.people = {n: {"role": None, "alive": True} for n in names}
        self.day = 0 
        self.history: list[str] = []  # for logging events in order

        self._assign_roles()
        print("人狼：",self._wolves())
        print("人狼：",self._seer())

    # ロールの割り当て
    def _assign_roles(self):
        names = list(self.people.keys())
        
        roles = [Wolf()] + [Madman()] + [Seer()] + [Villager()] * (len(names) - 3) 
        
        random.shuffle(roles)
        
        for name, role in zip(names, roles):
            self.people[name]["role"] = role    
    

    def kill(self):
        # Killの準備
        candidates = self._alive()
        werewolf_name  = self._wolves()[0] #人狼
        werewolf_role = self.people[werewolf_name]["role"]

        messages = werewolf_role.role_play_pormpt(candidates)

        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False)  # これで文字列になる
        # 出力
        target = self.llm.generate(prompt, self.sampling)[0].outputs[0].text.strip()

        
        # レーベンシュタイン距離で確実に判定
        victim = self.lenven(target)
        

        
        if victim == "":
            victim = "None"

        if self.people[victim]["alive"]:
            self.people[victim]["alive"] = False
            self._log(f"Night {self.day}: {victim} が死亡しました。")
            self.day += 1
        
        # 占い師
        seer_name  = self._seer()[0]
        seer_role = self.people[seer_name]["role"]

        if self.people[seer_name]["alive"] == True:
            messages = seer_role.role_play_pormpt(candidates,seer_name)

            prompt = self.tokenizer.apply_chat_template(messages, tokenize=False)  # これで文字列になる
            # 出力
            target = self.llm.generate(prompt, self.sampling)[0].outputs[0].text.strip()

            target = self.lenven(target)


            if target == "":
                divine_role = "失敗"
            else:
                divine_role = target + " -> " + str(self.people[target]["role"])
        else:
            divine_role = ""
            

        # killされた反応
        kill_reactions = self.react_to_death(victim)  

        # sus 誰が怪しい

        suspect_reaction = self.susupect(victim,kill_reactions)  

        return [victim,self._alive(),kill_reactions,suspect_reaction,divine_role]     
    


    # 誰かが殺された後、生存者たちが自分の潔白を主張する反応

    def react_to_death(self, victim: str):
        alive = self._alive()
        # ★生存者分まとめてバッチ生成
        prompts = [self.people[n]["role"].react_prompt_ja(victim) for n in alive]
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
        prompts = [self.people[n]["role"].sus_prompt_ja(victim,n,kill_reactions) for n in alive]
        results = self.llm.generate(prompts, self.sampling)
        
        # save reactions by dictionary
        all_reactions = {name:"" for name in alive}

        for name, res in zip(alive, results):
            line = res.outputs[0].text.strip()
            
            all_reactions[name] = line

            self._log(f"{name} の反応: 「{line}」")
        
        return all_reactions