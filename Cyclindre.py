import math

class Cylindre:
  last_id = -1
  type_param = {
    1: {
      'gain': 1,
      'masse': 1
    },
    2: {
      'gain': 2,
      'masse': 2
    },
    3: {
      'gain': 3,
      'masse': 2
    }
  }


  def __init__(self, x, y, type, rayon = 1):
    self.id = Cylindre.last_id + 1
    Cylindre.last_id += 1
    self.x = x
    self.y = y
    self.rayon = rayon
    self.type = None
    self.isActive = True
    self.connections = []
    self.type = int(type)
    self.gain = Cylindre.type_param[self.type]['gain']
    self.masse = Cylindre.type_param[self.type]['masse']

  def willCollide(self, cylindreDest, cylindreTest):
    # équation droite de départ vers destination
    a_eq = (cylindreDest.y - self.y) / (cylindreDest.x - self.x)
    b_eq = self.y - self.x * a_eq
    # équation de la perpendiculaire passant par le cylindre test
    a_perp = -1/a_eq
    b_perp = cylindreTest.y - a_perp * cylindreTest.x
    # coordonnees du point d'intersection des 2 droites
    x_inter = (b_perp - b_eq) / (a_eq - a_perp)
    y_inter = x_inter * a_eq + b_eq
    # vérifie si le point est dans les bornes min et max de départ et d'arrivée
    x_min = min(self.x, cylindreDest.x)
    x_max = max(self.x, cylindreDest.x)
    y_min = min(self.y, cylindreDest.y)
    y_max = max(self.y, cylindreDest.y)
    if not(x_min <= x_inter and x_inter <= x_max and y_min <= y_inter and y_inter <= y_max):
      return False
    # distance entre les points
    distance = math.sqrt((x_inter - cylindreTest.x)**2 + (y_inter - cylindreTest.y)**2)
    return distance <= cylindreTest.rayon + self.rayon
  
  def updateConnections(self, listCylindres, currentCylindre=None):
    self.connections = []
    for i in range(len(listCylindres)):
      # if currentCylindre != None:
      # if not listCylindres[i].isActive:
      #   flag = False
      #   break
      if i != self.id:
        flag = True
        for j in range(len(listCylindres)):
          if j != i and j != self.id:
            if self.willCollide(listCylindres[i], listCylindres[j]) and listCylindres[j].isActive:
              flag = False
        if flag:
          self.connections.append(i)

  def distance(self, cylindre):
    return math.sqrt((cylindre.x - self.x)**2 + (cylindre.y - self.y)**2)