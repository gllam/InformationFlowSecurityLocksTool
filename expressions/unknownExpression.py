from expressions.expression import Expression


class UnknownExpression(Expression):

  def __init__(self):
    pass
  
  def toString(self, level = 0):
    return "{space}-- Unknown Expression".format(space = '  ' * level)
  
  
  def evaluate(self):
    raise Exception("Unknown Expression cannot be evaluated!")


  