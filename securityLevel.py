from abc import abstractmethod


securityLevelsDictionary = {
  "bot" : 0,
  "l" : 1,
  "h" : 2,
  "top" : 3,
}

securityLevelsReverseDictionary = {
  0  : "bot",
  1 : "l",
  2 : "h",
  3 : "top",
}

class SecurityLevel:
  level: int
  
  def __init__(self, level):
    if isinstance(level, str):
      if level not in ["bot", "l", "h", "top"]:
        raise Exception("Security level not supported. Only supported ->", ["bot", "l", "h", "top"])
      self.level = securityLevelsDictionary[level]
      return
    
    if isinstance(level, int):
      if level not in [0,1,2,3]:
        raise Exception("Security level not supported. Only supported ->", ["bot", "l", "h", "top"])
      self.level = level
      return
    
    if isinstance(level, SecurityLevel):
      self.level = level.level
      return

  def isLessEqualThan(self, targetLevel):
    return self.level <= targetLevel.level

  def isGreaterEqualThan(self, targetLevel):
    return self.level >= targetLevel.level
  
  def join(self, targetLevel) -> int:
    return self.level if self.level > targetLevel.level else targetLevel.level

  def meet(self, targetLevel):
    return self.level if self.level < targetLevel.level else targetLevel.level
  
  def getLevelAsString(self) -> str:
    return securityLevelsReverseDictionary[self.level]
  
  @abstractmethod
  def getLevelByInt(level: int) -> str:
    return securityLevelsReverseDictionary[level]
      