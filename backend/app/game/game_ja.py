from vllm import LLM, SamplingParams
import torch

import random
from transformers import AutoTokenizer,AutoModelForCausalLM,pipeline
import Levenshtein
from transformers import set_seed
from roles.wolf import Wolf
from roles.villager import Villager

set_seed(548)

class Game:


    def __init__(self):

        self.llm = LLM(model="elyza/Llama-3-ELYZA-JP-8B-AWQ")  
        self.sampling = SamplingParams(temperature=0.8,
                                       top_p=0.95,
                                       max_tokens=40)
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

    #レーベンシュタイン距離で文字の編集距離を計算
    def lenven(self,target):
        names = self._villagers()
        max_name = ""
        max_score = 0
        for name in names:
            similarity = 1 - Levenshtein.distance(target, name) / max(len(target), len(name))
            if max_score<similarity:
                max_name = name
                max_score = similarity
        return max_name


    def _assign_roles(self):
        names = list(self.people.keys())
        
        roles = [Wolf()] + [Villager()] * (len(names) - 1)
        
        random.shuffle(roles)
        
        for name, role in zip(names, roles):
            self.people[name]["role"] = role    
    
    # 今生きている人
    def _alive(self):
        return [name for name, data in self.people.items() if data["alive"]]
    # 人狼の人
    def _wolves(self):
        return [n for n in self._alive() if isinstance(self.people[n]["role"],Wolf)]
    # 村人の人

    def _villagers(self):
        return [n for n in self._alive() if isinstance(self.people[n]["role"],Villager)]
    def _log(self, message: str):
        print(message)
        self.history.append(message)
    def _history(self):
        for history in self.history:
            print(history)
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

        self.react_to_death(target)       
    
    def vote(self):
        alive = self._alive()
        votes: dict[str, int] = {}
        
        for voter in alive:
            options = [p for p in alive if p != voter]
            choice = random.choice(options)
            votes[choice] = votes.get(choice, 0) + 1
        return votes

    def vote_kill(self,max_vote,target):
        # find max voted target; tie → random among top

        self.people[target]["alive"] = False
        self._log(
            f"Day {self.day}: 投票の結果 {target} が処刑されました (得票 {max_vote})。"
        )

    def react_to_death(self, victim: str):
        """誰かが殺された後、生存者たちが自分の潔白を主張する反応（instruct対応）"""
        alive = self._alive()
        # ★生存者分まとめてバッチ生成
        prompts = [self.people[n]["role"].react_prompt(victim) for n in alive]
        results = self.llm.generate(prompts, self.sampling)

        for name, res in zip(alive, results):
            line = res.outputs[0].text.strip()
            self._log(f"{name} の反応: 「{line}」")

