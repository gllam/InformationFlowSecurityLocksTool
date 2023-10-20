from typing import Any
from auxiliars import getAllIndexesOfSubstringInString
from expressions.expression import Expression
from programToEvaluate import ProgramToEvaluate
from securityLevel import SecurityLevel
from statements.statement import Statement


class Ref(Statement):
  variableToInitialize: Expression
  variableSecurityLevel: str
  value: Expression
  statement: Statement
  writeLevel: SecurityLevel = None
  terminationLevel: SecurityLevel = None
  line: int = None

  def __init__(self, sequenceText, separatorsIndexes, currentLine = 0):
    from customAst import CustomAST
    self.line = currentLine

    variableAndSecurityLevel = sequenceText[separatorsIndexes[0] + len("ref"):separatorsIndexes[1]].strip()
    variableSecurityLevel = variableAndSecurityLevel.split(",")[1]
    variableSecurityLevel = variableSecurityLevel[:len(variableSecurityLevel) - 1]
    self.variableSecurityLevel = variableSecurityLevel
    
    variable = variableAndSecurityLevel.split(",")[0]
    variable = variable[1:]
    #print("variable: " , variable)
    self.variableToInitialize = CustomAST.getAstExpression(variable, currentLine)
    
    #print("value: " , sequenceText[separatorsIndexes[1] + len("="):separatorsIndexes[2]])
    newLineNumber = currentLine + len(getAllIndexesOfSubstringInString(sequenceText[0: separatorsIndexes[1] + len("=")], '\n'))
    self.value = CustomAST.getAstExpression(sequenceText[separatorsIndexes[1] + len("="): separatorsIndexes[2]], newLineNumber)
    
    #print("statement: " , sequenceText[separatorsIndexes[2] + len("in"):len(sequenceText) - len(')')])
    newLineNumber = currentLine + len(getAllIndexesOfSubstringInString(sequenceText[0: separatorsIndexes[2] + len("in")], '\n'))
    self.statement = CustomAST.getAstStatement(sequenceText[separatorsIndexes[2] + len("in"): len(sequenceText) - len(')')], newLineNumber)

  def toString(self, level = 0):
    text =   "{space}-- [line {line}] Ref: {variable} = {value}\n{space}{space}in:\n{space}{statement}".format(line = self.line, variable= self.variableToInitialize.toString(level+1), value=self.value.toString(level+1), statement= self.statement.toString(level + 1), space = '  ' * level)
    return text
  
  def __getattribute__(self, __name: str) -> Any:
    if super().__getattribute__(__name) == None:
      if __name == "writeLevel" or __name == "terminationLevel":
        self.evaluate()
    
    return super().__getattribute__(__name)


  def evaluate(self): #TESTED WITH SUCCESS
    ProgramToEvaluate.addVariable(self.variableToInitialize, self.variableSecurityLevel, self.value.effectType)
    
    if not self.value.readLevel.isLessEqualThan(self.variableToInitialize.effectType.level):
      raise Exception("Value read security level ({}), needs to be less or equal than variable write level ({}) in \n{}".format(
        self.value.readLevel.getLevelAsString(),
        self.variableToInitialize.effectType.level.getLevelAsString(),
        self.toString()))
    
    self.writeLevel = SecurityLevel(self.variableToInitialize.effectType.level.meet(self.statement.writeLevel))
    self.terminationLevel = SecurityLevel(self.statement.terminationLevel)

    #print(self.writeLevel.getLevelAsString())
    #print(self.terminationLevel.getLevelAsString())

    