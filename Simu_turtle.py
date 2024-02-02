import turtle as t
from random import random

def simulate_turtle(instructions, quick=True):
  print(instructions)
  if not quick:
    t.speed(0.5)
  else:
     t.speed(10)
  t.setpos(0, 0)
  for instruction in instructions:
      if len(instruction.split()) > 1:
        ordre, valeur = instruction.split()
        valeur = float(valeur)
        if ordre == 'TURN':
          t.left(valeur)
        elif ordre == 'GO':
          t.fd(valeur*10)
          t.dot(10)
