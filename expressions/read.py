from expressions.effectType import EffectType
from expressions.expression import Expression
from typing import Any

from securityLevel import SecurityLevel


class Read(Expression):
    expression: Expression
    effectType: EffectType = None
    line: int = None
    
    def __init__(self, readText, currentLine):
        self.line = currentLine
        from customAst import CustomAST
        self.expression = CustomAST.getAstExpression(readText[1:], currentLine)

    def toString(self, level = 0):
        text =   "-- [line {line}] Read: {expression}".format(line= self.line, expression= self.expression.toString(level + 1))
        return text

    def __getattribute__(self, __name: str) -> Any:
        if super().__getattribute__(__name) == None:
            if __name == "effectType":
                self.evaluate()
        
        return super().__getattribute__(__name)
    
    def evaluate(self): #TESTED WITH SUCCESS!
        if not self.expression.effectType.isRef():
            raise Exception("{} needs to be ref".format(self.expression.toString()))
        
        self.effectType = EffectType(self.expression.effectType.type.level ,self.expression.effectType.type.type)
        self.readLevel = SecurityLevel(self.expression.readLevel.join(self.expression.effectType.level))