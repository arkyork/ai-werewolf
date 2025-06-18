from vllm import LLM, SamplingParams
import torch

import random
from transformers import AutoTokenizer,AutoModelForCausalLM,pipeline
import Levenshtein
from transformers import set_seed
from roles.wolf import Wolf
from roles.villager import Villager
from roles.seer import Seer


set_seed(548)

class Game:
    
    # 今生きている人
    def _alive(self):
        return [name for name, data in self.people.items() if data["alive"]]
    # 人狼の人
    def _wolves(self):
        return [n for n in self._alive() if isinstance(self.people[n]["role"],Wolf)]
        # 今生きている人
    def _seer(self):
        return [n for n in self._alive() if isinstance(self.people[n]["role"],Seer)]
    # 村人の人
    def _villagers(self):
        return [n for n in self._alive() if isinstance(self.people[n]["role"],Villager)]
    
    def _log(self, message: str):
        #print(message)
        self.history.append(message)
    
    def _history(self):
        for history in self.history:
            print(history)    
    
    #レーベンシュタイン距離で編集距離を計算
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

    # 投票処理
    def vote(self):
        alive = self._alive()
        votes: dict[str, int] = {}
        
        for voter in alive:
            options = [p for p in alive if p != voter]
            choice = random.choice(options)
            votes[choice] = votes.get(choice, 0) + 1
        return votes

    # 投票によるkill
    def vote_kill(self,max_vote,target):

        self.people[target]["alive"] = False
        self._log(
            f"Day {self.day}: 投票の結果 {target} が処刑されました (得票 {max_vote})。"
        )

        if self.end():
            print("end")

    # ゲームの終了条件
    
    def end(self):
        
        wolves = self._wolves()

        for wolf in wolves:
            if wolf["alive"] == True:
                return False
        
        return True

