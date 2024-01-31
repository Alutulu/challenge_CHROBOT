import turtle as t
from random import random

def simulate_turtle(instructions, quick=True):
  print(instructions)
  if not quick:
    t.speed(0.5)
  else:
     t.speed(10)
  t.setpos(0, 0)
  t.left(90)
  for instruction in instructions:
      ordre, valeur = instruction.split()
      valeur = float(valeur)
      # print('ordre :', ordre, ' | valeur :', valeur)
      if ordre == 'Turn':
        t.left(valeur)
      elif ordre == 'Go':
         t.fd(valeur*10)
         t.dot(10)
