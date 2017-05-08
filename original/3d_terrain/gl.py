from pyglet.gl import *
from variables import cube_size


def cube_points(x,y,z):
  n = cube_size
  x *= n*2
  y *= n*2
  z *= n*2
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



def draw_cube(x,y,z,n):
  glBegin(GL_QUADS)
  # top
  glVertex3f(x-n,y+n,z-n)
  glVertex3f(x+n,y+n,z-n)
  glVertex3f(x+n,y+n,z+n)
  glVertex3f(x-n,y+n,z+n)
  # bottom
  glVertex3f(x-n,y-n,z-n)
  glVertex3f(x+n,y-n,z-n)
  glVertex3f(x+n,y-n,z+n)
  glVertex3f(x-n,y-n,z+n)
  # front
  glVertex3f(x-n,y-n,z+n)
  glVertex3f(x+n,y-n,z+n)
  glVertex3f(x+n,y+n,z+n)
  glVertex3f(x-n,y+n,z+n)
  # back
  glVertex3f(x-n,y-n,z-n)
  glVertex3f(x+n,y-n,z-n)
  glVertex3f(x+n,y+n,z-n)
  glVertex3f(x-n,y+n,z-n)
  # left
  glVertex3f(x-n,y-n,z+n)
  glVertex3f(x-n,y-n,z-n)
  glVertex3f(x-n,y+n,z-n)
  glVertex3f(x-n,y+n,z+n)
  # right
  glVertex3f(x+n,y-n,z+n)
  glVertex3f(x+n,y-n,z-n)
  glVertex3f(x+n,y+n,z-n)
  glVertex3f(x+n,y+n,z+n)
  glEnd()