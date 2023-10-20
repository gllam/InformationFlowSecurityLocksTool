from typing import Any
from auxiliars import getAllIndexesOfSubstringInString
from expressions.expression import Expression
from securityLevel import SecurityLevel
from statements.statement import Statement


class Lock(Statement):
  pointer: Expression
  lockedStatement: Statement
  writeLevel: SecurityLevel = None
  terminationLevel: SecurityLevel = None
  line: str = None

  def __init__(self, sequenceText, separatorsIndexes, currentLine = 0):
    self.line = currentLine
    from customAst import CustomAST
    #print("pointer: " , sequenceText[separatorsIndexes[0] + len("lock"):separatorsIndexes[1]])
    self.pointer = CustomAST.getAstExpression(sequenceText[separatorsIndexes[0] + + len("while"):separatorsIndexes[1]], currentLine)
    
    #print("lockedStatement: " , sequenceText[separatorsIndexes[1] + len("in"):len(sequenceText) - len(')')])
    newLineNumber = currentLine + len(getAllIndexesOfSubstringInString(sequenceText[0: separatorsIndexes[1] + len("in")], '\n'))
    self.lockedStatement = CustomAST.getAstStatement(sequenceText[separatorsIndexes[1] + len("in"):len(sequenceText) - len(')')], newLineNumber)

  def toString(self, level = 0):
    text = "{space}-- [line {line}] Lock:\n{space}{space}pointer: {pointer}\n{space}{space}in:\n{space}{lockedStatement}".format(line = self.line, pointer= self.pointer.toString(level+1), lockedStatement=self.lockedStatement.toString(level+1), space = '  ' * level)
    return text


  def __getattribute__(self, __name: str) -> Any:
    if super().__getattribute__(__name) == None:
      if __name == "writeLevel" or __name == "terminationLevel":
        self.evaluate()
    
    return super().__getattribute__(__name)

  def evaluate(self): #TESTED WITH SUCCESS!
    if not self.pointer.effectType.isRef():
      raise Exception("Pointer needs to be a ref in:\n {}".format(self.toString()))
    
    #sigma <= ell_1
    if not self.pointer.readLevel.isLessEqualThan(self.pointer.effectType.level):
      raise Exception("Pointer read security level ({}), needs to be less or equal than pointer effect type level ({}) in \n{}".format(
        self.pointer.readLevel.getLevelAsString(),
        self.pointer.effectType.level.getLevelAsString(),
        self.toString()))
    
    #ell_1 <= ell
    if not self.pointer.effectType.level.isLessEqualThan(self.lockedStatement.writeLevel):
      raise Exception("Pointer effect type security level ({}), needs to be less or equal than statement write level ({}) in \n{}".format(
        self.pointer.effectType.level.getLevelAsString(),
        self.lockedStatement.writeLevel.getLevelAsString(),
        self.toString()))
    
    self.writeLevel = SecurityLevel(self.lockedStatement.writeLevel)
    self.terminationLevel = SecurityLevel(self.lockedStatement.terminationLevel.join(self.pointer.effectType.level))


    