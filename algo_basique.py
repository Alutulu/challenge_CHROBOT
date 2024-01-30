import math 
from main import *
from LireMap import lireMap
from Cyclindre import *
collecte = 0
temps = 300
solution = False
chemin = []

class Roomba:
  def __init__(self, x, y, rayon = 1, carburant = 10000, vitesse = 1, masse = 1):
    self.x = x
    self.y = y
    self.rayon = rayon
    self.carburant = carburant
    self.vitesse = vitesse
    self.masse = masse

def collecter(cylindre, roomba):
  global collecte
  global temps
  print("appel collecter()")
  roomba.masse += cylindre.masse #Ajout masse
  roomba.carburant -= (100+3*roomba.masse)*distance(cylindre, roomba) #Penalité carburant, j'ai pas la formule donc purement arbitraire 
  collecte += cylindre.gain #Ajout gain
  temps -= distance(cylindre, roomba)/roomba.vitesse #Décompte du temps avant MAJ vitesse
  roomba.vitesse = vitesse(roomba.masse) #MAJ Vitesse avec nouvelle masse
  roomba.x = cylindre.x #MAJ Position
  roomba.y = cylindre.y 
  print("nouvelle masse = ", roomba.masse," nouveau carburant = ", roomba.carburant," nouveau gain = ", collecte," temps restant = ", temps, "nouvelle vitesse = ", roomba.vitesse, "nouvelle position roomba : ",roomba.x, roomba.y)
  cylindre.isActive = False


def algo(roombatest, cylindres, temps):
    while(temps>0 and roombatest.carburant>0): #Tant qu'il reste du temps et du carburant
        if(collecte == 0): #Si c'est la première itération
            print("debug : collecte = 0")
            mindist = math.inf 
            for cylindre in cylindres: #Pour tous les cylindres de la map
                tempdist = distance(cylindre, roombatest) #calculer distance avec cylindre considéré
                print(tempdist)
                if tempdist < mindist:
                    print("maj mindist")
                    mindist = tempdist
                    cible = cylindre #maj cible
            collecter(cible, roombatest)
            chemin.append(cible.id)
        else:
            mincout = math.inf
            for id_cylindre in cible.connections:
                if cylindres[id_cylindre].isActive:
                    tempcout = distance(roombatest, cylindres[id_cylindre])-cylindres[id_cylindre].gain #Test completement naif
                    if tempcout<mincout:
                        mincout = tempcout
                        cible = cylindres[id_cylindre]
                        solution = True
            if(solution):
                collecter(cible, roombatest)
                chemin.append(cible.id)
                solution = False
            else:
                print("plus de solutions!")
                break   
    if(temps<0):
        print("Temps écoulé!")
    elif(roombatest.carburant<0):
        print("Plus d'essence!")
    print("chemin = ", chemin)
    return chemin   
       
def main_algo():
    roombatest = Roomba(0, 0)
    cylindres = []
    try:
        x, y, t = lireMap("donnees-map.txt")
    except:
        x, y, t = lireMap("C:/Users/thund/OneDrive/Documents/chrobo/challenge_CHROBOT/donnees-map.txt")
    for i in range(len(x)):
        cylindres.append(Cylindre(x[i], y[i], t[i]))
    # for cylindre in cylindres:
    #     print(cylindre.id, cylindre.x, cylindre.y, cylindre.masse, cylindre.gain)
    for i in range(len(cylindres)):
        cylindres[i].updateConnections(cylindres)
    temps = 300
    collecte = 0
    algo(roombatest, cylindres, temps)
    collecte = 0

if __name__ == "__main__":
    main_algo()