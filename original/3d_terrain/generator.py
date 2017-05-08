from queue import Queue
from threading import Thread
<<<<<<< HEAD
=======
from noise import snoise2
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39
from block import Block
from world import World
import variables


<<<<<<< HEAD
class Generator():
  def __init__(self,world,queue):
    self.thread = GeneratorThread(world,queue)
    self.queue = queue
    self.thread.start()


  def stop(self):
    self.thread.running = False
    self.queue.put((None,None,None))
=======
def map(v,mn,mx,nmn,nmx):
  r = v - mn
  r /= mx - mn
  r *= nmx - nmn
  r += nmn
  return r


class Generator():
  def __init__(self,world):
    self.queue = Queue(variables.max_generation_requests)
    self.world = world
    self.thread = GeneratorThread(self.world,self.queue)
    self.thread.start()


  def request_column(self,x,y):
    self.queue.put((x,y))


  def request_columns(self,x,y,x1,y1):
    for a in range(x,x1):
      for b in range(y,y1):
        self.request_column(a,b)


  def stop(self):
    self.thread.running = False
    self.queue.put((None,None))
    self.thread.join()
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39


class GeneratorThread(Thread):
  def __init__(self,world,queue):
    Thread.__init__(self)
    self.world = world
    self.queue = queue
    self.queue.maxsize = variables.max_generation_requests
    self.running = True


<<<<<<< HEAD
  def generate(self,x,y,z):
    block = Block(x=x,y=y,z=z,type="grass")
=======
  def generate_height(self,x,y):
    noise = snoise2(x/variables.x_scale,
                    y/variables.y_scale,
                    octaves=5,
                    persistence=0.5)*20
    #noise = map(noise,0,10,variables.z_min,variables.z_max)
    block_height = round(noise)
    return block_height


  def generate_type(self,x,y,z):
    block = Block(position=[x,y,z],type="grass")
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39
    self.world.set_block(x,y,z,block)


  def run(self):
<<<<<<< HEAD
    while (self.running):
      x,y,z = self.queue.get()
      if x != None and y != None and z != None:
        self.generate(x,y,z)
=======
    while self.running:
      x,y = self.queue.get()
      if x != None and y != None:
        h = self.generate_height(x,y)
        for z in range(variables.z_min,h):
          self.generate_type(x,y,z)
>>>>>>> 58dabf188b5386c398aedbf8703b5a9fd5f44a39
        self.queue.task_done()