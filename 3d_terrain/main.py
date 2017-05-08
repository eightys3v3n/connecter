import pyglet,math
<<<<<<< HEAD
from pyglet.gl import *
from math import floor
from time import time
from time import sleep
from noise import pnoise2
import variables,gl,world,player
=======
from sys import exit
from pyglet.gl import *
from math import floor
from threading import Thread
from time import time
from time import sleep
from noise import pnoise2
import variables,world,player,generator,block
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39


# increase performance
pyglet.options['debug_gl'] = False


class Window(pyglet.window.Window):
  def __init__(self):
    # initialize the window
<<<<<<< HEAD
    self.window = pyglet.window.Window()
    self.window.set_size(variables.pixel_width,variables.pixel_height)
    self.window.set_exclusive_mouse(True)
    self.window.set_vsync(False)

    # allows for a is_this_key_pressed check
    self.keys = pyglet.window.key.KeyStateHandler()
    self.window.push_handlers(self.keys)
=======
    super(Window,self).__init__()
    self.set_size(variables.pixel_width,variables.pixel_height)
    self.set_exclusive_mouse(True)
    self.set_vsync(False)

    # allows for a is_this_key_pressed check
    self.keys = pyglet.window.key.KeyStateHandler()
    self.push_handlers(self.keys)
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39

    self.world = world.World()
    self.player = player.PlayerManager()
    self.world_render = world.WorldRender()
<<<<<<< HEAD
    self.generator = generator.Generator()

    pyglet.clock.set_fps_limit(256)
    pyglet.clock.schedule_interval(self.prevent_sleep,1.0/60.0)
    pyglet.clock.schedule_interval(self.update_fps_counter,1.0/10.0)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    # don't draw any shape that is behind something
    # the "front" of a 2d shape is the side that means it was drawn counter clock wise
=======
    self.generator = generator.Generator(self.world)

    pyglet.clock.set_fps_limit(256)
    pyglet.clock.schedule_interval(self.prevent_sleep,1.0/60.0)
    #pyglet.clock.schedule_interval(self.reload_view,1.0)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39
    glEnable(GL_CULL_FACE)
    glFrontFace(GL_CCW)
    glCullFace(GL_BACK)

<<<<<<< HEAD

    self.world.generate_section(-10,-10,10,10)
    self.world.load_blocks(-10,-10,10,10)
=======
    b = block.Block(position=[0,0,0],type="grass")
    self.world_render.load_block(b)
    self.loaded_blocks = 0
    self.slow = False


  def quit(self):
    self.generator.stop()
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39


  # this is just to stop pyglet from sleeping the program
  def prevent_sleep(self,dt):
    pass


<<<<<<< HEAD
  def update_fps_counter(self,dt):
    self.fps.text = str(round(pyglet.clock.get_fps(),3))


  def check_user_input(self):
    direction = [0.0,0.0,0.0]
    if self.keys[pyglet.window.key.LEFT] or self.keys[pyglet.window.key.A]:
      direction[0] += variables.move_speed
    if self.keys[pyglet.window.key.RIGHT] or self.keys[pyglet.window.key.D]:
      direction[0] += -variables.move_speed
    if self.keys[pyglet.window.key.UP] or self.keys[pyglet.window.key.W]:
      direction[2] += variables.move_speed
    if self.keys[pyglet.window.key.DOWN] or self.keys[pyglet.window.key.S]:
      direction[2] += -variables.move_speed
    if self.keys[pyglet.window.key.SPACE]:
      direction[1] += -variables.move_speed
    if self.keys[pyglet.window.key.LSHIFT]:
      direction[1] += variables.move_speed
    self.player.move_relative(direction)
=======
  def reload_view(self,dt):
    if self.loaded_blocks > 80000:
      if not self.slow:
        self.slow = True
        self.player.player.position = [0.0,0.0,0.0]
      print("loaded blocks",self.loaded_blocks)
    count = 0
    x,y,x1,y1 = self.player.get_visible()
    for a in range(x,x1):
      for b in range(y,y1):
        if self.world.column_exists(a,b):
          column_pos = self.world.get_column_pos(a,b)
          for pos in column_pos:
            if not self.world.get_loaded(pos[0],pos[1],pos[2]):
              if count <= variables.blocks_per_frame:
                self.world_render.load_block(self.world.get_block(pos[0],pos[1],pos[2]))
                self.world.set_loaded(pos[0],pos[1],pos[2],1)
                self.loaded_blocks += 1
                count += 1
        else:
          self.generator.request_column(a,b)
    if self.loaded_blocks >= 80000:
      print("unloading all loaded blocks to avoid graphics glitch on my pc")
      self.world_render.unload_all()
      self.world.unload_all()
      self.loaded_blocks = 0
    #self.world_render.load_blocks(blocks)


  def check_user_input(self):
    x = 0.0
    y = 0.0
    z = 0.0
    if self.keys[pyglet.window.key.LEFT] or self.keys[pyglet.window.key.A]:
      x += variables.move_speed[0]
    if self.keys[pyglet.window.key.RIGHT] or self.keys[pyglet.window.key.D]:
      x += -variables.move_speed[0]
    if self.keys[pyglet.window.key.UP] or self.keys[pyglet.window.key.W]:
      y += variables.move_speed[1]
    if self.keys[pyglet.window.key.DOWN] or self.keys[pyglet.window.key.S]:
      y += -variables.move_speed[1]
    if self.keys[pyglet.window.key.SPACE]:
      z += -variables.move_speed[2]
    if self.keys[pyglet.window.key.LSHIFT]:
      z += variables.move_speed[2]
    if x or y or z:
      self.player.move(x,y,z)
      current = self.world.get_block_pos_at(self.player.get_position())
      #print("standing on",current)
      if current != self.player.standing_on():
        self.player.set_standing_on(current)


  def player_physics(self):
    if not self.player.flying:
      top_block_height = self.world.get_top_block_height(self.player.standing_on()[0],self.player.standing_on()[1])
      if top_block_height != None:
        if self.player.standing_on()[2] > top_block_height:
          print("falling")
          self.player.move(0,0,-variables.fall_speed[2])
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39


  def on_mouse_scroll(self,x,y,scroll_x,scroll_y):
    if scroll_y < 0:
<<<<<<< HEAD
      variables.field_of_view += 1
    elif scroll_y > 0:
      variables.field_of_view -= 1


  def on_mouse_motion(self,x,y,dx,dy):
    self.player.shift_heading(dy*variables.mouse_sensitivity[1],dx*variables.mouse_sensitivity[0])


  def on_key_press(self,symbol,modifiers):
    pass


  def on_draw(self):
    self.check_user_input()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    gluPerspective(variables.field_of_view, variables.pixel_width/variables.pixel_height, 0.1, 10000.0)
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    self.player.draw()
    self.world.draw()

    glDisable(GL_DEPTH_TEST)
    glTranslatef(0.0,0.0,-500.0)
    self.fps.x = -self.player.position[0]-variables.pixel_width/2
    self.fps.y = -self.player.position[1]
    self.fps.draw()
    glEnable(GL_DEPTH_TEST)

    glFlush()
=======
      variables.move_speed[0] -= 0.5
      variables.move_speed[1] -= 0.5
      variables.move_speed[2] -= 0.5
    elif scroll_y > 0:
      variables.move_speed[0] += 0.5
      variables.move_speed[1] += 0.5
      variables.move_speed[2] += 0.5

    for i in range(len(variables.move_speed)):
      if variables.move_speed[i] <= 0:
        variables.move_speed[i] = 0.01


  def on_mouse_motion(self,x,y,dx,dy):
    self.player.look(-dy*variables.mouse_sensitivity[0],dx*variables.mouse_sensitivity[1])

  def on_key_press(self,symbol,modifiers):
    if symbol == pyglet.window.key.F:
      self.player.flying = not self.player.flying


  def on_draw(self):
    self.reload_view(None)
    self.player_physics()
    self.check_user_input()

    self.clear()
    #glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    self.player.draw_perspective()
    self.world_render.draw()
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39


def main():
  window = Window()
  pyglet.app.run()
<<<<<<< HEAD
=======
  window.quit()
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39


if __name__ == "__main__":
  main()