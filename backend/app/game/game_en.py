import random
from transformers import AutoTokenizer,AutoModelForCausalLM,pipeline
import Levenshtein
from transformers import set_seed
from roles.wolf import Wolf
from roles.villager import Villager
from roles.seer import Seer
from roles.madman import Madman

from .game_base import Game


set_seed(548)

class Wolf_EN(Game):


    def __init__(self):
        names = [
            "Llama-3.1",
            "Llama-3.2",
            "Llama3",
            "tinyllama",
            "Mistral",
            "DeepSeek",
            "gemma",
            "Phi-4",
        ]
        self.people = {name: {"role": None, "alive": True,"model":None,"tokenizer":None} for name in names}
        self.day = 0 
        self.history: list[str] = []  # for logging events in order

        self._assign_roles()
        self._assign_models()
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
        
        roles = [Wolf()] +[Madman()]+[Seer()] + [Villager()] * (len(names) - 3)
        
        random.shuffle(roles)
        
        for name, role in zip(names, roles):
            self.people[name]["role"] = role
    
    def _assign_models(self):
        names = list(self.people.keys())
        for name in names:
            if name == "GPT2":
                tokenizer = AutoTokenizer.from_pretrained("dahara1/llama3.1-8b-Instruct-awq")
                model = AutoModelForCausalLM.from_pretrained("dahara1/llama3.1-8b-Instruct-awq",device_map="auto")
                self.people[name]["model"] = model
                self.people[name]["tokenizer"] = tokenizer

            if name == "Llama3":
                tokenizer = AutoTokenizer.from_pretrained("AMead10/Llama-3.2-1B-Instruct-AWQ")
                model = AutoModelForCausalLM.from_pretrained("AMead10/Llama-3.2-1B-Instruct-AWQ",device_map="auto")
                self.people[name]["model"] = model
                self.people[name]["tokenizer"] = tokenizer

            if name == "Llama3.1":
                tokenizer = AutoTokenizer.from_pretrained("AMead10/Llama-3.2-1B-Instruct-AWQ")
                model = AutoModelForCausalLM.from_pretrained("AMead10/Llama-3.2-1B-Instruct-AWQ",device_map="auto")
                self.people[name]["model"] = model
                self.people[name]["tokenizer"] = tokenizer

            if name == "Llama3.2":
                tokenizer = AutoTokenizer.from_pretrained("AMead10/Llama-3.2-1B-Instruct-AWQ")
                model = AutoModelForCausalLM.from_pretrained("AMead10/Llama-3.2-1B-Instruct-AWQ",device_map="auto")
                self.people[name]["model"] = model
                self.people[name]["tokenizer"] = tokenizer

            if name == "tinyllama":
                tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")

                model = AutoModelForCausalLM.from_pretrained("TheBloke/TinyLlama-1.1B-Chat-v0.3-AWQ",device_map="auto")
                self.people[name]["model"] = model
                self.people[name]["tokenizer"] = tokenizer          
            if name == "Mistral":
                tokenizer = AutoTokenizer.from_pretrained("AMead10/Llama-3.2-1B-Instruct-AWQ")
                model = AutoModelForCausalLM.from_pretrained("AMead10/Llama-3.2-1B-Instruct-AWQ",device_map="auto")
                self.people[name]["model"] = model
                self.people[name]["tokenizer"] = tokenizer                 
            if name == "DeepSeek":
                #tokenizer = AutoTokenizer.from_pretrained("casperhansen/deepseek-r1-distill-llama-8b-awq")
                #model = AutoModelForCausalLM.from_pretrained("casperhansen/deepseek-r1-distill-llama-8b-awq",device_map="auto")
                tokenizer = AutoTokenizer.from_pretrained("AMead10/Llama-3.2-1B-Instruct-AWQ")
                model = AutoModelForCausalLM.from_pretrained("AMead10/Llama-3.2-1B-Instruct-AWQ",device_map="auto")
                self.people[name]["model"] = model
                self.people[name]["tokenizer"] = tokenizer          
            if name == "gemma":
                #tokenizer = AutoTokenizer.from_pretrained("dangvansam/gemma-2-9b-it-fix-system-role-awq")
                #model = AutoModelForCausalLM.from_pretrained("dangvansam/gemma-2-9b-it-fix-system-role-awq")
                tokenizer = AutoTokenizer.from_pretrained("AMead10/Llama-3.2-1B-Instruct-AWQ")
                model = AutoModelForCausalLM.from_pretrained("AMead10/Llama-3.2-1B-Instruct-AWQ",device_map="auto")
                self.people[name]["model"] = model
                self.people[name]["tokenizer"] = tokenizer          

            if name == "Phi-4":
                #tokenizer = AutoTokenizer.from_pretrained("stelterlab/phi-4-AWQ")
                #model = AutoModelForCausalLM.from_pretrained("stelterlab/phi-4-AWQ")
                tokenizer = AutoTokenizer.from_pretrained("AMead10/Llama-3.2-1B-Instruct-AWQ")
                model = AutoModelForCausalLM.from_pretrained("AMead10/Llama-3.2-1B-Instruct-AWQ",device_map="auto")

                self.people[name]["model"] = model
                self.people[name]["tokenizer"] = tokenizer   


    
    def kill(self):
        # Killの準備
        candidates = self._alive()
        werewolf_name  = self._wolves()[0] #人狼
        werewolf_role = self.people[werewolf_name]["role"]

        #　モデルの準備
        model = self.people[werewolf_name]["model"]
        tokenizer = self.people[werewolf_name]["tokenizer"]
        generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

        messages = werewolf_role.role_play_prompt(candidates)

        # 出力
        result = generator(messages, do_sample=True, max_new_tokens=10)
        victim = result[0]["generated_text"][-1]["content"].strip()
        
        # レーベンシュタイン距離で確実に判定
        victim = self.lenven(victim)
        

        if self.people[victim]["alive"]:
            self.people[victim]["alive"] = False
            self._log(f"Night {self.day}: {victim} が死亡しました。")
            self.day += 1

        # 占い師
        seer_name  = self._seer()[0]
        seer_role = self.people[seer_name]["role"]

        if self.people[seer_name]["alive"] == True:
            messages = seer_role.role_play_prompt(candidates,seer_name)
            model = self.people[seer_name]["model"]
            tokenizer = self.people[seer_name]["tokenizer"]
            generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
            
            result = generator(messages, do_sample=True, max_new_tokens=10)
            # 出力
            target = result[0]["generated_text"][-1]["content"].strip()

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
        # save reactions by dictionary
        all_reactions = {name:"" for name in alive}


        for name in alive:
            model = self.people[name]["model"]
            tokenizer = self.people[name]["tokenizer"]
            if not model or not tokenizer:
                self._log(f"{name} はそっと沈黙を守った（モデル未設定）")
                continue

            role = self.people[name]["role"]

            prompt = role.react_prompt_en(victim)


            generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
            
            result = generator(prompt, do_sample=True, temperature=0.95, top_p=0.95, max_new_tokens=40)
            generated = result[0]["generated_text"].strip().split("\n")[-1]

            all_reactions[name] = generated

            self._log(f"{name} の反応: 「{generated}」")

            

        return all_reactions

    def susupect(self,victim,kill_reactions):
        alive = self._alive()
        # save reactions by dictionary
        sus_reactions = {name:"" for name in alive}
        


        for name in alive:
            model = self.people[name]["model"]
            tokenizer = self.people[name]["tokenizer"]
            if not model or not tokenizer:
                self._log(f"{name} はそっと沈黙を守った（モデル未設定）")
                continue

            role = self.people[name]["role"]



            generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
            
            prompt = role.sus_prompt_en(victim,name,kill_reactions)

            result = generator(prompt, do_sample=True, temperature=0.95, top_p=0.95, max_new_tokens=40)
            generated = result[0]["generated_text"].strip().split("\n")[-1]

            sus_reactions[name] = generated

            self._log(f"{name} の反応: 「{generated}」")

            

        return sus_reactions
