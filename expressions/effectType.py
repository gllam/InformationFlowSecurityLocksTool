from securityLevel import SecurityLevel


class EffectType:
  level: SecurityLevel
  type: any
  
  def __init__(self, level, type):
    if isinstance (level, SecurityLevel):
      self.level = SecurityLevel(level.level)
    else:
      self.level = SecurityLevel(level)
    
    if type != "int":
      if isinstance (type, EffectType):
        self.type = type
        return
      if type.find(";") != -1: #TESTED WITH SUCCESS
        securityLevel = type.split(";",1)[1].split(",")[0]
        newType = type.split(";",1)[1].split(",",1)[1]
        self.type = EffectType("bot", newType) #level of int in effectType is always bot 
        return
      raise Exception("Type {} not supported. Only valid types -> {}".format(type, ["int", "ref"]))
    
    self.type = type

  def isRef(self):
    return self.type != "int"
  
  def isInt(self):
    return self.type == "int"
  
  def toInputSchemaString(self):
    if isinstance(self.type, str):
      return "{},{}".format(self.level.getLevelAsString(),self.type)
    
    if isinstance(self.type, EffectType):
      return "{},ref;{}".format(self.level.getLevelAsString(),self.type.toInputSchemaString())

  
    

    