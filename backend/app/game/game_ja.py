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
from roles.knight import Knight
from roles.fox import Fox
from roles.medium import Medium
from roles.baker import Baker

from .game_base import Game

class Wolf_JA(Game):

    def __init__(self):

        self.llm = LLM(model="tokennext/llama-3-8b-elyza-ja-werewolf-awq")  
        self.sampling = SamplingParams(temperature=0.8,
                                       top_p=0.95,
                                       max_tokens=120)
        self.role_sampling = SamplingParams(temperature=0.8,
                                top_p=0.92,
                                max_tokens=40)
        self.tokenizer = AutoTokenizer.from_pretrained("elyza/Llama-3-ELYZA-JP-8B-AWQ")
        
        names = ["たろう", "じろう", "さぶろう", "しんじ", "けんた", "ゆうこ", "あかね", "みさき", "りょう", "はるか"]

        self.people = {n: {"role": None, "alive": True} for n in names}
        self.day = 0 
        self.history: list[str] = []  # for logging events in order
        self.medium_checked = set() 
        self.seer_checked = set() 

        self._assign_roles()

    # ロールの割り当て
    def _assign_roles(self):
        names = list(self.people.keys())
        
        assign ={
            "wolf" : random.randint(1,2),
            "seer" : random.randint(0,1),
            "madman" : random.randint(0,1),
            "knight" : random.randint(0,1),
            "baker" : random.randint(0,1),
            "medium" : random.randint(0,1),
            "fox" : random.randint(0,1),

        }
        role_num = sum([value for key,value in assign.items()])
        # 役割
        roles = [Knight()]*assign["knight"]+[Fox()]*assign["fox"]+[Baker()]*assign["baker"]+[Medium()]*assign["medium"]+[Wolf()]*assign["wolf"] + [Madman()]*assign["madman"] + [Seer()]*assign["seer"] + [Villager()] * (len(names) - role_num) 
        
        random.shuffle(roles)
        
        for name, role in zip(names, roles):
            self.people[name]["role"] = role    
    
    def seer_play(self):
        candidates = [name for name in self._alive() if name not in self.seer_checked]
        
        divine_role = "失敗"
        # 占い師
        for seer_name in  self._seer():
            seer_role = self.people[seer_name]["role"]

            if self.people[seer_name]["alive"] == True:
                prompt = seer_role.role_play_prompt_ja(candidates,seer_name)



                output = self.llm.generate(prompt, self.role_sampling)

                target = output[0].outputs[0].text.strip()


                target = self.lenven(target)




                if target == "":
                    divine_role = "失敗"
                elif  str(self.people[target]["role"]) == "FOX":
                    self.people[target]["alive"] = False
                    divine_role = target + " -> VILLAGER"
                else:
                    divine_role = target + " -> " + str(self.people[target]["role"])

                self.seer_checked.add(target)

            else:
                divine_role = ""
            

        return divine_role
    def wolf_play(self,protected):
        # Killされる候補
        candidates = self._not_wolves()
        
        #被害者たち
        victims = []
        
        # 人狼によるkill
        for werewolf_name in self._wolves():
            werewolf_role = self.people[werewolf_name]["role"]

            prompt = werewolf_role.role_play_prompt_ja(candidates)

            # プロンプト
            target = self.llm.generate(prompt, self.role_sampling)[0].outputs[0].text.strip()
            
            # レーベンシュタイン距離で確実に判定
            victim = self.lenven(target)

            if victim in protected:
                self._log(f"Night day {self.day}:  {werewolf_name}は{victim} をねらっていたようだ。")
                self._log(f"Night day {self.day}: {victim} は騎士によって守られた")
                
                continue

            # killの動作
            if self.people[victim]["alive"]:
                self.people[victim]["alive"] = False
                self._log(f"Night day {self.day}:  {werewolf_name}によって {victim} が死亡しました。")
            
            # 被害者の追加
            victims.append(victim)

            # 今回は人狼が一人殺すように設定
            break

        return victims
    def baker_play(self):
        # パン屋の処理
        breads_num = 0
        for baker in self._bakers():
            breads_num += 1

        return breads_num
    def medium_play(self):
        # killされた人
        candidates = [name for name in self._not_alive() if name not in self.medium_checked]
        
        die_role = "失敗"
        # 誰も死んでない
        if len(candidates) == 0:
            return die_role+" : 誰も死んでいないようだ"
        # 霊媒師
        for medium_name in  self._medium():
            medium_role = self.people[medium_name]["role"]

            if self.people[medium_name]["alive"]: # -> 霊媒師が生きているなら
                
                prompt = medium_role.role_play_prompt_ja(candidates)

                # 出力
                target = self.llm.generate(prompt, self.role_sampling)[0].outputs[0].text.strip()
                target = self.lenven(target,role="MEDIUM")




                if target == "":
                    die_role = "失敗"
                elif  str(self.people[target]["role"]) == "FOX":
                    die_role = target + " -> VILLAGER"
                else:
                    die_role = target + " -> " + str(self.people[target]["role"])

                self.medium_checked.add(target)

            else:
                die_role = ""
        return die_role
    
    def knight_play(self):
        # Killされる候補
        candidates = self._alive()
        
        protected = []
        
        # 人狼によるkill
        for knight_name in self._knights():
            knight_role = self.people[knight_name]["role"]

            prompt = knight_role.role_play_prompt_ja(candidates,knight_name)
            # 出力
            target = self.llm.generate(prompt, self.sampling)[0].outputs[0].text.strip()
            
            
            # レーベンシュタイン距離で確実に判定
            protect_name = self.lenven(target)
            
            # 被害者の追加
            protected.append(protect_name)

            self._log(f"{knight_name}は{protect_name}を守った")
        
        return protected
    
    def kill(self):

        protected = self.knight_play()
        
        victims = self.wolf_play(protected)
        victim = ",".join(victims)
        
        divine_role = self.seer_play()
        
        breads_num = self.baker_play()

        die_role = self.medium_play()

        # killされた反応
        kill_reactions = self.react_to_death(victim)  

        # sus 誰が怪しい

        suspect_reaction = self.susupect(victim,kill_reactions,die_role)  
        

        self.day += 1
        
        data={
            "victim":victims,
            "alive":self._alive(),
            "kill_reactions":kill_reactions,
            "sus_reactions":suspect_reaction,
            "divine_role":divine_role,
            "bread_num":breads_num,
            "die_role":die_role
        }

        self._history()

        return data    
    


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

            #self._log(f"{name} の反応: 「{line}」")

        return all_reactions

    def susupect(self,victim,kill_reactions,die_role):
        alive = self._alive()


        # 生存者分まとめて生成
        prompts = [self.people[n]["role"].sus_prompt_ja(victim,n,kill_reactions,die_role) if str(self.people[n]["role"]) == "SEER" else self.people[n]["role"].sus_prompt_ja(victim,n,kill_reactions) for n in alive ]
        results = self.llm.generate(prompts, self.sampling)
        
        # save reactions by dictionary
        all_reactions = {name:"" for name in alive}

        for name, res in zip(alive, results):
            line = res.outputs[0].text.strip()
            
            all_reactions[name] = line

            #self._log(f"{name} の反応: 「{line}」")
        
        return all_reactions