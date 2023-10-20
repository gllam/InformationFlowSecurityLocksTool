from typing import Any
from statements.statement import Statement


class UnknownStatement(Statement):

  def __init__(self):
    pass
  
  def toString(self, level = 0):
    return "{space}-- Unknown Statement".format(space = '  ' * level)
  
  def __getattribute__(self, __name: str) -> Any:
    if super().__getattribute__(__name) == None:
      if __name == "writeLevel" or __name == "terminationLevel":
        self.evaluate()
    
    return super().__getattribute__(__name)
  
  def evaluate(self):
    raise Exception("Unknown Statement cannot be evaluated!")


  