from polymer import parallel_iterators
import time
import multiprocessing

class Iterator(object):
  def __init__(self, internal):
    self.internal = internal
  
  def iter(self, callback):
    pool = multiprocessing.Pool(processes = 1)
    pool.map(inner, self.internal)

  def __iter__(self):
    return self.internal.__iter__()

class Entry(object):
  @classmethod
  def all(self):
    return Iterator(xrange(0, 5))

@parallel_iterators
def parallel_thingy():
  print "Start parallel"
  
  for entry in Entry.all():
    time.sleep(1)

def serial_thingy():
  print "Start serial"

  for entry in Entry.all():
    time.sleep(1)

if __name__ == '__main__':
  parallel_thingy()
  serial_thingy()
