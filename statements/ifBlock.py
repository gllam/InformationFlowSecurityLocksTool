from typing import Any
from auxiliars import getAllIndexesOfSubstringInString
from expressions.expression import Expression
from securityLevel import SecurityLevel
from statements.statement import Statement


class IfBlock(Statement):
  condition: Expression
  thenBlock: Statement
  elseBlock: Statement
  writeLevel: SecurityLevel = None
  terminationLevel: SecurityLevel = None
  line: int = None

  def __init__(self, sequenceText, separatorsIndexes, currentLine):
    from customAst import CustomAST
    self.line = currentLine
    #print("condition: " , sequenceText[separatorsIndexes[0] + len("if"):separatorsIndexes[1]])
    newLineNumber = currentLine + len(getAllIndexesOfSubstringInString(sequenceText[0: separatorsIndexes[0] + len("if")], '\n'))
    self.condition = CustomAST.getAstExpression(sequenceText[separatorsIndexes[0] + len("if"):separatorsIndexes[1]], newLineNumber)
    
    #print("thenBlock: " , sequenceText[separatorsIndexes[1] + len("then"):separatorsIndexes[2]])
    newLineNumber = currentLine + len(getAllIndexesOfSubstringInString(sequenceText[0: separatorsIndexes[1] + len("then")], '\n'))
    self.thenBlock = CustomAST.getAstStatement(sequenceText[separatorsIndexes[1] + len("then"):separatorsIndexes[2]], newLineNumber)
    
    #print("elseBlock: " , sequenceText[separatorsIndexes[2] + len("else"):len(sequenceText) - len(')')])
    newLineNumber = currentLine + len(getAllIndexesOfSubstringInString(sequenceText[0: separatorsIndexes[2] + len("else")], '\n'))
    self.elseBlock = CustomAST.getAstStatement(sequenceText[separatorsIndexes[2] + len("else"):len(sequenceText) - len(')')], newLineNumber)

  def toString(self, level = 0):
    text =   "{space}-- [line {line}] IfBlock:\n{space}{space}condition:\n{space}{condition}\n{space}{space}then:\n{space}{then}\n{space}{space}else:\n{space}{elseBlock}".format(line = self.line, condition= self.condition.toString(level+1), then=self.thenBlock.toString(level+1), elseBlock= self.elseBlock.toString(level + 1), space = '  ' * level)
    return text

  def __getattribute__(self, __name: str) -> Any:
    if super().__getattribute__(__name) == None:
      if __name == "writeLevel" or __name == "terminationLevel":
        self.evaluate()
    
    return super().__getattribute__(__name)

  def evaluate(self): #TESTED WITH SUCCESS!
    if not self.condition.effectType.isInt():
      raise Exception("Condition needs to be an int in:\n {}".format(self.toString()))
    
    #sigma <= ell_1
    if not self.condition.readLevel.isLessEqualThan(self.thenBlock.writeLevel):
      raise Exception("Condition security read level ({}), needs to be less or equal than then block statement write level ({}) in \n{}".format(
        self.condition.readLevel.getLevelAsString(),
        self.thenBlock.writeLevel.getLevelAsString(),
        self.toString()))
    
    #sigma <= ell_2
    if not self.condition.readLevel.isLessEqualThan(self.elseBlock.writeLevel):
      raise Exception("Condition read security level ({}), needs to be less or equal than else block statement write level ({}) in \n{}".format(
        self.condition.readLevel.getLevelAsString(),
        self.elseBlock.writeLevel.getLevelAsString(),
        self.toString()))
    
    self.writeLevel = SecurityLevel(self.thenBlock.writeLevel.meet(self.elseBlock.writeLevel))
    ifStatementsSecurityLevel = SecurityLevel(self.thenBlock.terminationLevel.join(self.elseBlock.terminationLevel))
    self.terminationLevel = SecurityLevel(self.condition.readLevel.join(ifStatementsSecurityLevel))
    
    #("{} meet {} = {}".format(
    #  self.thenBlock.writeLevel.getLevelAsString(),
    #  self.elseBlock.writeLevel.getLevelAsString(),
    #  self.writeLevel.getLevelAsString()
    #))

    #print("{} join {} join {} = {}".format(
    #  self.condition.effectType.level.getLevelAsString(),
    #  self.thenBlock.terminationLevel.getLevelAsString(),
    #  self.elseBlock.terminationLevel.getLevelAsString(),
    #  self.terminationLevel.getLevelAsString()
    #))

    