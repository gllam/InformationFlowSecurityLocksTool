from expressions.effectType import EffectType
from expressions.expression import Expression
from securityLevel import SecurityLevel


class IntegerConstant(Expression):
    effectType: EffectType

    def __init__(self, value, currentLine = 0):
        try :
            self.value = int(value)
        except :
            raise Exception("Integer constant needs to be an integer: {}".format(value))
        self.effectType = EffectType("bot", "int")
        self.readLevel = SecurityLevel("bot")

    def toString(self, level = 0):
      return "{value} ({type})".format(value= self.value, type= self.effectType.type)

    def evaluate(self):
        pass