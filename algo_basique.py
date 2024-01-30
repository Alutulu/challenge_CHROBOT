import math 
import main
collecte = 0
temps = 300

class Roomba:
  def __init__(self, x, y, rayon = 1, carburant = 10000, vitesse = 12, masse = 1):
    self.x = x
    self.y = y
    self.rayon = rayon
    self.carburant = carburant
    self.vitesse = vitesse
    self.masse = masse

def collecter(cylindre, roomba):
  roomba.masse += cylindre.masse #Ajout masse
  roomba.carburant -= main.distance(cylindre, roomba)*roomba.masse*0.5 #Penalité carburant, j'ai pas la formule donc purement arbitraire 
  collecte += cylindre.gain #Ajout gain
  temps -= main.distance(cylindre, roomba)/roomba.vitesse #Décompte du temps avant MAJ vitesse
  roomba.vitesse = main.vitesse(roomba.masse) #MAJ Vitesse avec nouvelle masse
  roomba.x = cylindre.x #MAJ Position
  roomba.y = cylindre.y 


def algo(roombatest, cylindres, temps, carburant):
  while(temps>0): #Tant qu'il reste du temps
    if(collecte == 0): #Si c'est la première itération
      mindist = math.inf 
      for cylindre in cylindres: #Pour tous les cylindres de la map
        tempdist = main.distance(cylindre, roombatest) #calculer distance avec cylindre considéré
        if tempdist > mindist:
          mindist = tempdist
          cible = cylindre #maj cible
      collecter(cylindres[cible], roombatest)
    else:
     coutmin = math.inf
     for cylindre in cylindres[cible].connections:
       
