import random
from Cyclindre import Cylindre

def genererRandomCylindres(nbCylindres=20, xmax=25, ymax=25, min_margin=3, printTxt=True):
  listCylindres = []
  for n in range(nbCylindres):
    spawned = False
    nb_iter = 0
    while not spawned and nb_iter <= 100:
      nb_iter += 1
      x = round(random.random() * xmax, 4)
      y = round(random.random() * ymax, 4)
      t = random.randint(1, 3)
      new_cylindre = Cylindre(x, y, t)
      trop_proche = False
      for cylindre in listCylindres:
        if new_cylindre.distance(cylindre) < min_margin:
          trop_proche = True
          break
      if not trop_proche:
        listCylindres.append(new_cylindre)
        spawned = True
      else:
        Cylindre.last_id -= 1
  if(printTxt):
    with open('C:/challenge/donnees-map.txt', 'w') as file:
        for cylindre in listCylindres:
            file.writelines(str(cylindre.x) + ' ' + str(cylindre.y) + ' ' + str(float(cylindre.type)) + '\n')
  return listCylindres