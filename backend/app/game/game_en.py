import random
from transformers import AutoTokenizer,AutoModelForCausalLM,pipeline
import Levenshtein
from transformers import set_seed
from roles.wolf import Wolf
from roles.villager import Villager

set_seed(548)

class Game:


    def __init__(self):
        names = [
            "GPT2",
            "llama3",
            "tinyllama",
            "Mistral",
            "DeepSeek",
            "gemma",
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
        
        roles = [Wolf()] + [Villager()] * (len(names) - 1)
        
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

            if name == "llama3":
                tokenizer = AutoTokenizer.from_pretrained("AMead10/Llama-3.2-1B-Instruct-AWQ")
                model = AutoModelForCausalLM.from_pretrained("AMead10/Llama-3.2-1B-Instruct-AWQ",device_map="auto")
                self.people[name]["model"] = model
                self.people[name]["tokenizer"] = tokenizer

            if name == "tinyllama":
                tokenizer = AutoTokenizer.from_pretrained("TheBloke/TinyLlama-1.1B-Chat-v0.3-AWQ")
                tokenizer.chat_template = (
                    "<|system|>\n{system_message}</s>\n"
                    "<|user|>\n{prompt}</s>\n"
                    "<|assistant|>\n"
                )
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

        #　モデルの準備
        model = self.people[werewolf_name]["model"]
        tokenizer = self.people[werewolf_name]["tokenizer"]
        generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

        messages = werewolf_role.role_play_pormpt(candidates)

        # 出力
        result = generator(messages, do_sample=True, max_new_tokens=10)
        target = result[0]["generated_text"][-1]["content"].strip()
        
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
        for name in alive:
            model = self.people[name]["model"]
            tokenizer = self.people[name]["tokenizer"]
            if not model or not tokenizer:
                self._log(f"{name} はそっと沈黙を守った（モデル未設定）")
                continue

            role = self.people[name]["role"]

            prompt = role.react_prompt(victim)


            generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
            
            result = generator(prompt, do_sample=True, temperature=0.95, top_p=0.95, max_new_tokens=40)
            generated = result[0]["generated_text"].strip().split("\n")[-1]

            self._log(f"{name} の反応: 「{generated}」")
