class Block():
<<<<<<< HEAD
  def __init__(self,x=None,y=None,z=None,type=None):
    self.x = x
    self.y = y
    self.z = z
    self.type = type
=======
  def __init__(self,position=[None,None,None],type=None):
    self.position = position
    self.type = type
    self.loaded = False


  def __str__(self):
    return str(self.position[0])+","+str(self.position[1])+","+str(self.position[2])+",type:"+str(self.type)
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39
