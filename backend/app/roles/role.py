from abc import ABCMeta
from abc import abstractclassmethod

class Role(metaclass = ABCMeta):
    @abstractclassmethod
    def react_prompt(self):
        pass
    @abstractclassmethod
    def role_play_pormpt(self):
        pass
