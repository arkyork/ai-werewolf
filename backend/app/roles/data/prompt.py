from abc import ABCMeta
from abc import abstractclassmethod

class Prompt(metaclass = ABCMeta):
    @abstractclassmethod
    def sus_play_prompt_ja():
        pass
    @abstractclassmethod
    def sus_play_prompt_en():
        pass
    @abstractclassmethod
    def react_prompt():
        pass