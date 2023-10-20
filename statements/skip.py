from securityLevel import SecurityLevel
from statements.statement import Statement


class Skip(Statement):
  writeLevel: SecurityLevel
  terminationLevel: SecurityLevel

  def __init__(self):
    self.writeLevel = SecurityLevel("top")
    self.terminationLevel = SecurityLevel("bot")

  def toString(self, level = 0):
    return "{space}-- Skip".format(space = '  ' * level)


  def evaluate(self):
    pass #nothing to do

    