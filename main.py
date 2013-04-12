from polymer import parallel_iterators

class Iterator(object):
  def __init__(self, internal):
    self.internal = internal
  
  def iter(self, callback):
    for i in self.internal:
      callback(i)

class Entry(object):
  @classmethod
  def all(self):
    return Iterator(xrange(0, 1000))

@parallel_iterators
def main():
  print "Before loop"
  
  for entry in Entry.all():
    print entry
  
  print "After loop"

if __name__ == '__main__':
  main()
