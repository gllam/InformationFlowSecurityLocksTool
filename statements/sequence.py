from typing import Any
from securityLevel import SecurityLevel
from statements.statement import Statement


class Sequence(Statement):
  leftStatement: Statement
  rightStatement: Statement
  writeLevel: SecurityLevel = None
  terminationLevel: SecurityLevel = None
  line: int = None

  def __init__(self, sequenceText, semicolonindex, currentLine = 0):
    from customAst import CustomAST
    self.line = currentLine
    from auxiliars import getAllIndexesOfSubstringInString
    self.leftStatement = CustomAST.getAstStatement(sequenceText[:semicolonindex], currentLine)
    
    newLineNumber = currentLine + len(getAllIndexesOfSubstringInString(sequenceText[:semicolonindex + 1], '\n'))
    self.rightStatement = CustomAST.getAstStatement(sequenceText[semicolonindex + 1:], newLineNumber)

  def toString(self, level = 0):
    text =   "{space}-- [line {line}] Sequence:\n{space}{left}\n{space}{right}".format(line = self.line, left= self.leftStatement.toString(level+1), right=self.rightStatement.toString(level+1), space = '  ' * level)
    return text

  def __getattribute__(self, __name: str) -> Any:
    if super().__getattribute__(__name) == None:
      if __name == "writeLevel" or __name == "terminationLevel":
        self.evaluate()
    
    return super().__getattribute__(__name)

  def evaluate(self): #TESTED WITH SUCCESS!
    if not self.leftStatement.terminationLevel.isLessEqualThan(self.rightStatement.writeLevel):
      raise Exception("Left statement termination level ({}), needs to be less or equal than right statement write level ({}) in \n{}".format(
        self.leftStatement.terminationLevel.getLevelAsString(),
        self.rightStatement.writeLevel.getLevelAsString(),
        self.toString()))

    self.writeLevel = SecurityLevel(self.leftStatement.writeLevel.meet(self.rightStatement.writeLevel))
    self.terminationLevel = SecurityLevel(self.leftStatement.terminationLevel.join(self.rightStatement.terminationLevel))

    