from typing import Any
from auxiliars import getAllIndexesOfSubstringInString
from expressions.expression import Expression
from securityLevel import SecurityLevel
from statements.statement import Statement


class Assignment(Statement):
  pointer: Expression
  value: Expression
  writeLevel: SecurityLevel = None
  terminationLevel: SecurityLevel = None
  line: int = None

  def __init__(self, sequenceText, attributionCharIndex, currentLine = 0):
    self.line = currentLine
    from customAst import CustomAST
    self.pointer = CustomAST.getAstExpression(sequenceText[:attributionCharIndex], currentLine)
    newLineNumber = currentLine + len(getAllIndexesOfSubstringInString(sequenceText[0: attributionCharIndex + 2], '\n'))
    self.value = CustomAST.getAstExpression(sequenceText[attributionCharIndex + 2:], newLineNumber) # len(':=') = 2

  def toString(self, level = 0):
    text =   "{space}-- [line {line}] Assignment:\n{space}{space}| {pointer}\n{space}{space}| {value}".format(
      line = self.line,
      pointer= self.pointer.toString(level+1),
      value= self.value.toString(level+1),
      space = '  ' * level)
    return text
  
  def __getattribute__(self, __name: str) -> Any:
    if super().__getattribute__(__name) == None:
      if __name == "writeLevel" or __name == "terminationLevel":
        self.evaluate()
    
    return super().__getattribute__(__name)
  
  def evaluate(self): #TESTED WITH SUCCESS
    if self.pointer.effectType.isInt():
      raise Exception("Pointer needs to be ref in -> {}".format(self.toString()))
    
    #print(self.pointer.toString())
    #print(self.pointer.effectType.level.getLevelAsString())

    #sigma_1 <= ell_1
    if not self.pointer.readLevel.isLessEqualThan(self.pointer.effectType.level):
      raise Exception("Pointer read level ({}), needs to be less or equal than pointer type level ({}) in \n{}".format(
        self.pointer.readLevel.getLevelAsString(),
        self.pointer.effectType.level.getLevelAsString(),
        self.toString()))
    
    #sigma_2 <= ell_1
    if not self.value.readLevel.isLessEqualThan(self.pointer.effectType.level):
      raise Exception("Value read level ({}), needs to be less or equal than pointer type level ({}) in \n{}".format(
        self.value.readLevel.getLevelAsString(),
        self.pointer.effectType.level.getLevelAsString(),
        self.toString()))
    
    self.terminationLevel = SecurityLevel("bot")
    self.writeLevel = SecurityLevel(self.pointer.effectType.level)

  