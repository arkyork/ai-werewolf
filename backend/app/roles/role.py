from abc import ABCMeta
from abc import abstractclassmethod

class Role(metaclass = ABCMeta):
    @abstractclassmethod
    def react_prompt_ja(self):
        pass
    @abstractclassmethod
    def react_prompt_en(self):
        pass
    @abstractclassmethod
    def react_prompt_en(self):
        pass
    @abstractclassmethod
    def role_play_prompt(self):
        pass
    @abstractclassmethod
    def sus_prompt_ja(self):
        pass
    @abstractclassmethod
    def sus_prompt_en(self):
        pass