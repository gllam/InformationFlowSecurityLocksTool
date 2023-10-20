from typing import Any
from auxiliars import getAllIndexesOfSubstringInString
from expressions.expression import Expression
from securityLevel import SecurityLevel
from statements.statement import Statement


class Spawn(Statement):
  spawnStatement: Statement
  writeLevel: SecurityLevel = None
  terminationLevel: SecurityLevel = None
  line: str = None

  def __init__(self, sequenceText, separatorsIndexes, currentLine = 0):
    self.line = currentLine
    from customAst import CustomAST
    #print("spawnStatement: " , sequenceText[separatorsIndexes[0] + len("spawn"):len(sequenceText) - len(')')])
    newLineNumber = currentLine + len(getAllIndexesOfSubstringInString(sequenceText[0: separatorsIndexes[0] + len("spawn")], '\n'))
    self.spawnStatement = CustomAST.getAstStatement(sequenceText[separatorsIndexes[0] + len("spawn"):len(sequenceText) - len(')')], newLineNumber)

  def toString(self, level = 0):
    text = "{space}-- [line {line}] Spawn:\n{space}{spawnStatement}".format(line = self.line, spawnStatement=self.spawnStatement.toString(level+1), space = '  ' * level)
    return text


  def __getattribute__(self, __name: str) -> Any:
    if super().__getattribute__(__name) == None:
      if __name == "writeLevel" or __name == "terminationLevel":
        self.evaluate()
    
    return super().__getattribute__(__name)
  
  def evaluate(self): #TESTED WITH SUCCESS!    
    self.writeLevel = SecurityLevel(self.spawnStatement.writeLevel)
    self.terminationLevel = SecurityLevel("bot")

  
    