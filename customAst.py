
from programToEvaluate import ProgramToEvaluate
from statements.lock import Lock
from statements.ref import Ref
from statements.skip import Skip
from expressions.integerConstant import IntegerConstant
from expressions.operation import Operation
from expressions.pointer import Pointer
from expressions.read import Read
from expressions.unknownExpression import UnknownExpression
from statements.assignment import Assignment
from expressions.expression import Expression
from statements.ifBlock import IfBlock
from statements.spawn import Spawn
from statements.unknownStatement import UnknownStatement
from statements.sequence import Sequence
from auxiliars import isAssignment, isIfBlock, isIntegerConstant, isLock, isOperation, isPointer, isRead, isRef, isSequence, isSkip, isSpawn, isWhileStatement
from statements.statement import Statement
from statements.whileStatement import WhileStatement

class CustomAST:

  @staticmethod
  def getAstStatement(programText: str, currentLine: int = 0) -> Statement:
    numberOfEnters = 0
    for char in programText:
      if char == '\n':
        numberOfEnters += 1
        continue
      if char == ' ' or char == '':
        continue 
      else:
        break
    
    currentLine += numberOfEnters
    programText = programText.strip()


    separatorsIndexes = isSequence(programText)
    if separatorsIndexes[0] != -1:
      return Sequence(programText, separatorsIndexes[0], currentLine)
    
    separatorsIndexes = isAssignment(programText)
    if separatorsIndexes[0] != -1:
      return Assignment(programText, separatorsIndexes[0], currentLine)
    
    separatorsIndexes = isIfBlock(programText)
    if separatorsIndexes[0] != -1 and separatorsIndexes[1] != -1 and separatorsIndexes[2] != -1:
      return IfBlock(programText, separatorsIndexes, currentLine)
    
    separatorsIndexes = isWhileStatement(programText)
    if separatorsIndexes[0] != -1 and separatorsIndexes[1] != -1:
      return WhileStatement(programText, separatorsIndexes, currentLine)
    
    separatorsIndexes = isSpawn(programText)
    if separatorsIndexes[0] != -1:
      return Spawn(programText, separatorsIndexes, currentLine)
    
    separatorsIndexes = isLock(programText)
    if separatorsIndexes[0] != -1 and separatorsIndexes[1] != -1:
      return Lock(programText, separatorsIndexes, currentLine)
    
    separatorsIndexes = isRef(programText)
    if separatorsIndexes[0] != -1 and separatorsIndexes[1] != -1 and separatorsIndexes[2] != -1:
      return Ref(programText, separatorsIndexes, currentLine)
    
    separatorsIndexes = isSkip(programText)
    if separatorsIndexes[0] != -1:
      return Skip()
    
    
    return UnknownStatement()
  
  @staticmethod
  def getAstExpression(expressionText: str, currentLine: int, variableSecurityLevel: str = None) -> Expression:
    numberOfEnters = 0
    for char in expressionText:
      if char == '\n':
        numberOfEnters += 1
        continue
      if char == ' ' or char == '':
        continue 
      else:
        break
    
    currentLine += numberOfEnters
    expressionText = expressionText.strip()
    
    #(e op e)
    separatorindex = isOperation(expressionText)
    if separatorindex[0] != -1:
      return Operation(expressionText, separatorindex[0], separatorindex[1], currentLine)
    
    #!e
    separatorindex = isRead(expressionText)
    if separatorindex[0] != -1:
      return Read(expressionText, currentLine)
   
    # n -> integer
    separatorindex = isIntegerConstant(expressionText)
    if separatorindex[0] != "error":
      return IntegerConstant(separatorindex[0], currentLine)
    
    # pointer or variable = letras sem espaços no meio
    separatorindex = isPointer(expressionText)
    if separatorindex[0] != -1:
      return Pointer(expressionText, currentLine, variableSecurityLevel)

    return UnknownExpression()
  