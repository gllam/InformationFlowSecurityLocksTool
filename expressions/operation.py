from typing import Any
from auxiliars import getAllIndexesOfSubstringInString
from expressions.effectType import EffectType
from expressions.expression import Expression
from securityLevel import SecurityLevel


class Operation(Expression):
    operator: str
    leftExpression: Expression
    rightExpression: Expression
    effectType: EffectType = None
    line: int = None
    
    def __init__(self, sequenceText, operationindex, operator, currentLine):
        self.operator = operator
        self.line = currentLine
        from customAst import CustomAST
        self.leftExpression = CustomAST.getAstExpression(sequenceText[1:operationindex], currentLine)
        newLineNumber = currentLine + len(getAllIndexesOfSubstringInString(sequenceText[0: operationindex + len(operator)], '\n'))
        self.rightExpression = CustomAST.getAstExpression(sequenceText[operationindex + len(operator):len(sequenceText) - 1], newLineNumber)

    def toString(self, level = 0):
        text =   "{space}-- [line {line}] Operation ({operator}):\n{space}{space}| {leftExpression}\n{space}{space}| {rightExpression}".format(line = self.line, operator=self.operator, leftExpression= self.leftExpression.toString(level+1), rightExpression= self.rightExpression.toString(level+1), space = '  ' * level)
        return text

    def evaluate(self): #TESTED WITH SUCCESS! 
        if self.leftExpression.effectType.isRef():
            raise Exception("{} needs to be an int in:\n".format(
                self.leftExpression.toString(),
                self.toString()
                ))
        
        if self.rightExpression.effectType.isRef():
            raise Exception("{} needs to be an int in:\n".format(
                self.rightExpression.toString(),
                self.toString()
                ))
    
        self.effectType = EffectType("bot", "int")
        self.readLevel = SecurityLevel(self.leftExpression.readLevel.join(self.rightExpression.readLevel))
        
    def __getattribute__(self, __name: str) -> Any:
        if super().__getattribute__(__name) == None:
            if __name == "effectType":
                self.evaluate()
        
        return super().__getattribute__(__name)