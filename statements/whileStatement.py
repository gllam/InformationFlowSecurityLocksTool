from typing import Any
from auxiliars import getAllIndexesOfSubstringInString
from expressions.expression import Expression
from securityLevel import SecurityLevel
from statements.statement import Statement


class WhileStatement(Statement):
  condition: Expression
  doStatement: Statement
  writeLevel: SecurityLevel = None
  terminationLevel: SecurityLevel = None
  line: int = None

  def __init__(self, sequenceText, separatorsIndexes, currentLine):
    self.line = currentLine
    from customAst import CustomAST
    #print("condition: " , sequenceText[separatorsIndexes[0] + len("while"):separatorsIndexes[1]])
    newLineNumber = currentLine + len(getAllIndexesOfSubstringInString(sequenceText[0: separatorsIndexes[0] + len("while")], '\n'))
    self.condition = CustomAST.getAstExpression(sequenceText[separatorsIndexes[0] + len("while"):separatorsIndexes[1]], newLineNumber)
    
    #print("statement: " , sequenceText[separatorsIndexes[1] + len("do"):len(sequenceText) - len(')')])
    newLineNumber = currentLine + len(getAllIndexesOfSubstringInString(sequenceText[0: separatorsIndexes[1] + len("do")], '\n'))
    self.doStatement = CustomAST.getAstStatement(sequenceText[separatorsIndexes[1] + len("do"):len(sequenceText) - len(')')], newLineNumber)

  def toString(self, level = 0):
    text = "{space}-- [line {line}] While:\n{space}{space}condition:\n{space}{condition}\n{space}{space}do:\n{space}{doStatement}".format(line = self.line, condition= self.condition.toString(level+1), doStatement=self.doStatement.toString(level+1), space = '  ' * level)
    return text

  def __getattribute__(self, __name: str) -> Any:
    if super().__getattribute__(__name) == None:
      if __name == "writeLevel" or __name == "terminationLevel":
        self.evaluate()
    
    return super().__getattribute__(__name)

  def evaluate(self): #TESTED WITH SUCCESS!
    if not self.condition.effectType.isInt():
      raise Exception("Condition needs to be an int in:\n {}".format(self.toString()))
    
    #sigma U kappa
    compareSecurityLevel = SecurityLevel(self.condition.readLevel.join(self.doStatement.terminationLevel))
    
    #sigma U kappa <= ell
    if not compareSecurityLevel.isLessEqualThan(self.doStatement.writeLevel):
      raise Exception("Condition read security level ({}) union with statement termination level ({}): ({}), needs to be less or equal than statement write level ({}) in \n{}".format(
        self.condition.readLevel.getLevelAsString(),
        self.doStatement.terminationLevel.getLevelAsString(),
        compareSecurityLevel.getLevelAsString(),
        self.doStatement.writeLevel.getLevelAsString(),
        self.toString()))
    
    self.writeLevel = SecurityLevel(self.doStatement.writeLevel)
    self.terminationLevel = SecurityLevel(self.condition.readLevel.join(self.doStatement.terminationLevel))

    #print("{} join {} = {}".format(
    #  self.condition.effectType.level.getLevelAsString(),
    #  self.doStatement.terminationLevel.getLevelAsString(),
    #  self.terminationLevel.getLevelAsString()
    #))