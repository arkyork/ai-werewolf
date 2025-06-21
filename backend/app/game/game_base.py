from vllm import LLM, SamplingParams
import torch

import random
from transformers import AutoTokenizer,AutoModelForCausalLM,pipeline
import Levenshtein
from transformers import set_seed
from roles.wolf import Wolf
from roles.villager import Villager
from roles.seer import Seer
from roles.baker import Baker
from roles.knight import Knight
from roles.fox import Fox
from roles.medium import Medium
set_seed(548)

class Game:
    

    # 今生きている人
    def _alive(self) -> list:
        return [name for name, data in self.people.items() if data["alive"]]
    def _not_alive(self) -> list:
        return [name for name, data in self.people.items() if not data["alive"]]

    # 人狼の人
    def _wolves(self) -> list:
        return [n for n in self._alive() if isinstance(self.people[n]["role"],Wolf)]
    # 人狼でない人
    def _not_wolves(self) -> list:
        return list(set(self._alive())-set(self._wolves()))
    # 今生きている人
    def _seer(self) -> list:
        return [n for n in self._alive() if isinstance(self.people[n]["role"],Seer)]
    # 村人の人
    def _villagers(self) -> list:
        return [n for n in self._alive() if isinstance(self.people[n]["role"],Villager)]
    # パン屋の人
    def _bakers(self) -> list:
        return [n for n in self._alive() if isinstance(self.people[n]["role"],Baker)]
    # 狐の人
    def _foxs(self) -> list:
        return [n for n in self._alive() if isinstance(self.people[n]["role"],Fox)]
    # 騎士の人
    def _knights(self) -> list:
        return [n for n in self._alive() if isinstance(self.people[n]["role"],Knight)]
    # 霊媒師の人
    def _medium(self) -> list:
        return [n for n in self._alive() if isinstance(self.people[n]["role"],Medium)]
    # ログ
    def _log(self, message: str):
        self.history.append(message)
    
    def _history(self):
        for history in self.history:
            print(history)    
    
    #レーベンシュタイン距離で編集距離を計算
    def lenven(self,target: str,role = None):

        if role == "MEDIUM":
            names = self._not_alive()
        else:
            names = self.people


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
    def vote_kill(self,target: str):

        self.people[target]["alive"] = False
        self._log(
            f"Day {self.day}: 投票の結果 {target} が処刑されました 。"
        )

