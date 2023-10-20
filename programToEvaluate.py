from expressions.effectType import EffectType
from expressions.expression import Expression
from expressions.pointer import Pointer
from securityLevel import SecurityLevel
from statements.statement import Statement


class ProgramToEvaluate:
  statement: Statement = None
  variables = {}

  @staticmethod
  def evaluate():
    try:
      ProgramToEvaluate.statement.evaluate()
      print("Program is safe!")
    except Exception as e:
      print("Error!\n{}".format(e))
    #ProgramToEvaluate.statement.evaluate()
  
  @staticmethod
  def startAst(programText: str):
    from customAst import CustomAST
    ProgramToEvaluate.statement = CustomAST.getAstStatement(programText, 1)
  
  @staticmethod
  def loadImportedVariables(importedVariablesText: str):
    importedVariablesSplitted = importedVariablesText.split('\n')
    for importedVariable in importedVariablesSplitted:
      securityLevel = importedVariable.split(":")[1].split(",")[0]
      type = importedVariable.split(":")[1].split(",",1)[1]
      ProgramToEvaluate.variables[importedVariable.split(":")[0]] = EffectType(securityLevel, type)

  @staticmethod
  def addVariable(variable: Expression, securityLevel: str, effectTypeOfValueAssignedToVariable: EffectType):
    if not isinstance(variable, Pointer):
      raise Exception("Variable in ref({},{}) needs to be of type ref".format(variable.toString(), securityLevel))
    
    if variable.name in ProgramToEvaluate.variables.keys():
      raise Exception("Cannot declare variable that it is already declared")
    
    ProgramToEvaluate.variables[variable.name] = EffectType(securityLevel, "ref;{}".format(effectTypeOfValueAssignedToVariable.toInputSchemaString()))
  
  @staticmethod
  def removeVariable(variable: Expression):
    if not isinstance(variable, Pointer):
      raise Exception("Variable ro be removed needs to be of type ref")
    
    if variable.name not in ProgramToEvaluate.variables.keys():
      raise Exception("Cannot remove variable {} because it does not exist in this scope".format(variable.name))
    
    ProgramToEvaluate.variables.pop(variable.name)
  
  def toString():
    return ProgramToEvaluate.statement.toString()