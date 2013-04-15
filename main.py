from polymer import parallel_iterators
import time
import types
import multiprocessing
import sys
import marshal

class CannotReadValues(object):
  pass

class Shared(object):
  def __init__(self, internal):
    members = [ (k, getattr(internal, k)) for k in dir(internal) ]
    
    self._internal = internal
    self._modifications = [ ]
    self._methods = dict([ (k, v) for (k, v) in members if callable(v) ])
    
    print self.methods
  
  def __getattribute__(self, name):
    if name in ('_internal', '_modifications', '_methods'):
      return object.__getattribute__(self, name)
    
    def invoke(*vargs, **dargs):
      self._modifications.append(*vargs, **dargs)
    
    return invoke

class Iterator(object):
  def __init__(self, internal):
    self.internal = internal
  
  def iter(self, callback):
    global_queue = multiprocessing.Queue()
    
    def make_cell(x):
      def inner(): return x
      return inner.func_closure[0]
    
    # copied_code = marshal.loads(marshal.dumps(callback.func_code))
    # cells = marshal.loads(marshal.dumps([ x.cell_contents for x in callback.func_closure or [ ] ]))
    # reconstituted = tuple( make_cell(x) for x in cells )
    
    # func = types.FunctionType(copied_code, globals = globals(), closure = reconstituted, name = '<init>')
    
    def kernel(q):
      while True:
        next = q.get()
        if next == 'STOP':
          break
        callback(next)
    
    processes = [ ]
    
    for i in xrange(multiprocessing.cpu_count()):
      processes.append(multiprocessing.Process(target = kernel, args = (global_queue,)))
    
    for process in processes:
      process.start()
    
    for item in self.internal:
      global_queue.put(item)
    
    for process in processes:
      global_queue.put('STOP')
    
    for process in processes:
      process.join()

  def __iter__(self):
    return self.internal.__iter__()

class Entry(object):
  @classmethod
  def all(self):
    return Iterator(xrange(0, 5))

def outer():
  outer = False
  
  @parallel_iterators
  def parallel_thingy():
    print "Start parallel"
    
    accum = Shared([ ])
    
    if False:
      parallel_thingy()
    
    # def inner(x):
    #   time.sleep(1)
    #   accum.append("Foo")
    # 
    # Entry.all().iter(inner)
    
    for entry in Entry.all():
      time.sleep(1)
      # print outer
      accum.append("Foo")
    
    print 'Accum: ', accum
  
  return parallel_thingy()

def serial_thingy():
  print "Start serial"
  
  accum = [ ]
  
  for entry in Entry.all():
    time.sleep(1)
    accum.append("Foo")
  
  print 'Accum: ', accum

if __name__ == '__main__':
  outer()
  serial_thingy()
