from typing import Any
from expressions.effectType import EffectType
from expressions.expression import Expression
from securityLevel import SecurityLevel


class Pointer(Expression):
    effectType: EffectType = None

    def __init__(self, value, currentLine, variableSecurityLevel):
        try :
            self.name = int(value)
        except:
            self.name = value
            if variableSecurityLevel != None:
                self.readLevel = SecurityLevel(variableSecurityLevel)
            else:
                self.readLevel = self.effectType.level
            return
        
        
        raise Exception("Pointer can't be an integer: {}".format(value))

    def toString(self, level = 0):
      return "{name} (ref)".format(name= self.name)

    def evaluate(self):
        pass

    def __getattribute__(self, __name: str) -> Any:
        if super().__getattribute__(__name) == None:
            if __name == "effectType":
                from programToEvaluate import ProgramToEvaluate
                try:
                    self.effectType = ProgramToEvaluate.variables[self.name]
                except:
                    raise Exception("Variable '{}' does not exist! Have you declared it in the document or using ref?".format(self.name))
        
        return super().__getattribute__(__name)