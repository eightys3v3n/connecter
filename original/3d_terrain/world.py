import pyglet
from pyglet.gl import *
from noise import pnoise2
<<<<<<< HEAD
import variables,gl


def noise(x,y):
  return pnoise2(x/10,y/10,octaves=1)*10


def block_height(x,z):
  return round(noise(x,z))
=======
from math import ceil
import variables
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39


class World:
  def __init__(self):
    self.world = {}
<<<<<<< HEAD
    self.batch = pyglet.graphics.Batch()
    self.faces = {}
    self.faces["bottom"] = pyglet.graphics.OrderedGroup(0)
    self.faces["back"] = pyglet.graphics.OrderedGroup(1)
    self.faces["left"] = pyglet.graphics.OrderedGroup(2)
    self.faces["right"] = pyglet.graphics.OrderedGroup(3)
    self.faces["front"] = pyglet.graphics.OrderedGroup(4)
    self.faces["top"] = pyglet.graphics.OrderedGroup(5)
    #self.set_block(0,0,0,variables.block["grass"])
    #self.load_block(0,0,0)
    #self.set_block(1,0,0,variables.block["grass"])
    #self.load_block(1,0,0)
=======
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39


  def block_exists(self,x,y,z):
    if x not in self.world:
      self.world[x] = {}
      return False
    if y not in self.world[x]:
      self.world[x][y] = {}
      return False
    if z not in self.world[x][y]:
      return False
    return True


<<<<<<< HEAD
  def set_block(self,x,y,z,v):
=======
  def column_exists(self,x,y):
    if x not in self.world:
      return False
    if y not in self.world[x]:
      return False
    for z in self.world[x][y]:
      if not self.block_exists(x,y,z):
        return False
    return True


  def set_block(self,x,y,z,block):
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39
    if x not in self.world:
      self.world[x] = {}
    if y not in self.world[x]:
      self.world[x][y] = {}

<<<<<<< HEAD
    self.world[x][y][z] = v
    return False


  def get_block_type(self,x,y,z):
    if not self.block_exists(x,y,z):
      return -1
    return self.world[x][y][z]


  def get_top_block(self,x,y):
=======
    self.world[x][y][z] = block
    return False


  def set_loaded(self,x,y,z,v):
    if x not in self.world:
      return None
    if y not in self.world[x]:
      return None

    self.world[x][y][z].loaded = v


  def get_loaded(self,x,y,z):
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39
    if x not in self.world:
      return None
    if y not in self.world[x]:
      return None
<<<<<<< HEAD
    top = None
    for z in self.world[x][y]:
      if top == None:
        top = z
      elif z > top:
        top = z
    return [x,y,z]


  def unload_all(self):
    self.batch = pyglet.graphics.Batch()


  def load_block(self,x,y,z):
    if not self.block_exists(x,y,z):
      return

    a = gl.cube_points(x,y,z)
    c = variables.block_colour[self.get_block_type(x,y,z)]

    self.batch.add_indexed(24,GL_QUADS,None,
      [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
      ("v3f",a),
      ("c3B",c))

#    self.batch.add_indexed(4,pyglet.gl.GL_POLYGON,self.faces["top"],
#      [0,1,2,3],
#      ("v3f",a[0:12]),
#      ("c3B",c[0:12])
#      )
#    self.batch.add_indexed(4,pyglet.gl.GL_POLYGON,self.faces["front"],
#      [0,1,2,3],
#      ("v3f",a[12:24]),
#      ("c3B",c[12:24])
#      )
#    self.batch.add_indexed(4, pyglet.gl.GL_POLYGON,self.faces["bottom"],
#      [0,1,2,3],
#      ("v3f",a[24:36]),
#      ("c3B",c[24:36])
#      )
#    self.batch.add_indexed(4, pyglet.gl.GL_POLYGON,self.faces["left"],
#      [0,1,2,3],
#      ("v3f",a[36:48]),
#      ("c3B",c[36:48])
#      )
#    self.batch.add_indexed(4, pyglet.gl.GL_POLYGON,self.faces["back"],
#      [0,1,2,3],
#      ("v3f",a[48:60]),
#      ("c3B",c[48:60])
#      )
#    self.batch.add_indexed(4, pyglet.gl.GL_POLYGON,self.faces["right"],
#      [0,1,2,3],
#      ("v3f",a[60:72]),
#      ("c3B",c[60:72])
#      )


  def load_top_block(self,x,y):
    if x not in self.world:
      return
    if y not in self.world[x]:
      return
=======

    return self.world[x][y][z].loaded


  def unload_all(self):
    for x in self.world:
      for y in self.world[x]:
        for z in self.world[x][y]:
          self.set_loaded(x,y,z,0)


  def get_block(self,x,y,z):
    if not self.block_exists(x,y,z):
      return None
    return self.world[x][y][z]


  def get_block_pos_at(self,position):
    x = -position[0]/variables.cube_size/2
    y = -position[1]/variables.cube_size/2
    z = -position[2]/variables.cube_size/2
    x = round(x)
    y = round(y)
    z = round(z)
    return [x,y,z]


  def get_top_block_height(self,x,y):
    if not self.column_exists(x,y):
      return None
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39
    top = None
    for z in self.world[x][y]:
      if top == None:
        top = z
      elif z > top:
        top = z
<<<<<<< HEAD
    self.load_block(x,y,z)


  def load_column(self,x,y):
    if x not in self.world:
      return
    if y not in self.world[x]:
      return
    for z in self.world[x][y]:
      self.load_block(x,y,z)


  def load_blocks(self,x,y,x1,y1):
    for a in range(x,x1):
      for b in range(y,y1):
        self.load_column(a,b)


  def generate_section(self,x,z,x1,z1):
    for a in range(x,x1):
      for b in range(z,z1):
        y = block_height(a,b)
        self.set_block(a,y,b,variables.block["grass"])
        for i in range(0,y-1):
          self.set_block(a,i,b,variables.block["stone"])


#  def draw(self,x,z,x1,z1):
#    for a in range(x,x1):
#      if a in self.world:
#        for b in range(z,z1):
#          if b in self.world[a]:
#            for c in self.world[a][b]:
#              if self.world[a][b][c] in variables.block_colour:
#                colour = variables.block_colour[self.world[a][b][c]]
#              else:
#                colour = [255,255,255]
#              glColor3d(colour[0],colour[1],colour[2])
#              self.draw_block(a,b,c)

  def draw(self):
=======
    return top


  def get_column(self,x,y):
    blocks = []
    if x not in self.world:
      return None
    if y not in self.world[x]:
      return None
    for z in self.world[x][y]:
      blocks.append(self.world[x][y][z])
    return blocks


  def get_column_pos(self,x,y):
    blocks = []
    if x not in self.world:
      return None
    if y not in self.world[x]:
      return None
    for z in self.world[x][y]:
      blocks.append([x,y,z])
    return blocks


class WorldRender():
  def __init__(self):
    self.batch = pyglet.graphics.Batch()


  def block_vertices(self,block):
    n = variables.cube_size
    x = block.position[0]*n*2
    y = block.position[2]*n*2
    z = block.position[1]*n*2
    return (
    # top
    x-n,y+n,z+n,
    x+n,y+n,z+n,
    x+n,y+n,z-n,
    x-n,y+n,z-n,
    # front
    x-n,y-n,z+n,
    x+n,y-n,z+n,
    x+n,y+n,z+n,
    x-n,y+n,z+n,
    # bottom
    x-n,y-n,z-n,
    x+n,y-n,z-n,
    x+n,y-n,z+n,
    x-n,y-n,z+n,
    # left
    x-n,y+n,z+n,
    x-n,y+n,z-n,
    x-n,y-n,z-n,
    x-n,y-n,z+n,
    # back
    x-n,y+n,z-n,
    x+n,y+n,z-n,
    x+n,y-n,z-n,
    x-n,y-n,z-n,
    # right
    x+n,y-n,z+n,
    x+n,y-n,z-n,
    x+n,y+n,z-n,
    x+n,y+n,z+n)


  def block_colour(self,block):
    return variables.block_colour[variables.block[block.type]]


  def unload_all(self):
    self.batch = pyglet.graphics.Batch()


  def load_block(self,block):
    a = self.block_vertices(block)
    c = self.block_colour(block)

    self.batch.add_indexed(24,GL_QUADS,None,
      [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
      ("v3f",a),
      ("c3B",c))


  def load_blocks(self,blocks):
    for block in blocks:
      self.load_block(block)


  def draw(self):
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39
    self.batch.draw()