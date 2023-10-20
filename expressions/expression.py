from abc import ABC, abstractmethod

from expressions.effectType import EffectType
from securityLevel import SecurityLevel


class Expression(ABC):
    readLevel: SecurityLevel = SecurityLevel("bot")
    effectType: EffectType = None

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def toString(self, level):
        pass