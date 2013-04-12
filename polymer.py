import byteplay

def parallel_iterators(function):
  source = byteplay.Code.from_code(main.func_code).code
  
  result_block = byteplay.Code.from_code(main.func_code)
  
  result = result_block.code
  result[:] = [ ]
  
  skip_n_instructions = 0
  
  for index, (opcode, argument) in enumerate(source):
    
    if skip_n_instructions > 0:
      skip_n_instructions -= 1
      continue
    
    if opcode == byteplay.FOR_ITER:
      
      inside_this_loop = [ ]
      
      for op, arg in source[index + 1:]:
        if op == argument: # loop destination
          break
        else:
          inside_this_loop.append((op, arg))
      
      inside_this_loop.pop() # remove JUMP_ABSOLUTE
      
      def created_inner_function(__fixme):
        pass
      
      new_code_block = byteplay.Code.from_code(created_inner_function.func_code)
      
      source_lines_break_stuff = [ (x, y) for (x, y) in inside_this_loop if x != byteplay.SetLineno ]
      
      new_code_block.code = (
        [(byteplay.LOAD_FAST, '__fixme')] +
        source_lines_break_stuff +
        [(byteplay.LOAD_CONST, None),
         (byteplay.RETURN_VALUE, None)]
      )
      
      result.pop() # remove label
      result.pop() # remove GET_ITER
      
      result.extend([
        (byteplay.LOAD_ATTR, "iter"),
        (byteplay.LOAD_CONST, new_code_block),
        (byteplay.MAKE_FUNCTION, 0),
        (byteplay.CALL_FUNCTION, 1),
        (byteplay.POP_TOP, None)
      ])
      
      skip_n_instructions = len(inside_this_loop) + 3
      
    elif opcode == byteplay.SETUP_LOOP:
      
      pass # FIXME
      
    else:
      
      result.append((opcode, argument))
  
  function.func_code = result_block.to_code()
  return function
