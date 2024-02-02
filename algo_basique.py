import math 
import numpy as np
from main import *
from LireMap import lireMap
from Cyclindre import *
from AfficherMap import afficherMap
from GenererMap import genererRandomCylindres
from Planifie import calculeAngle 

import numpy as np
from main import v0, a, distance
collecte = 0
temps = 300
solution = False
chemin = []
sommep = 0

class Roomba:
  def __init__(self, x, y, rayon = 1, carburant = 10000, vitesse = 1, masse = 1):
    self.x = x
    self.y = y
    self.rayon = rayon
    self.carburant = carburant
    self.vitesse = vitesse
    self.masse = masse
    self.direction = np.array([1, 0])
    
    def calculeVitesse(self)  -> float:
        return v0*np.exp(-a*self.masse)
    
    def distanceCylindre(self, cyl) -> float:
        return distance(self, cyl)

def collecter(cylindre, roomba):
  global collecte
  global temps
  global sommep
  print("appel collecter()")
  roomba.carburant -= (100+3*roomba.masse)*distance(cylindre, roomba) * 0.969999
  roomba.masse += cylindre.masse #Ajout masse
   #Penalité carburant, j'ai pas la formule donc purement arbitraire 
  collecte += cylindre.gain #Ajout gain
  angle = calculeAngle(roomba.direction, roomba, cylindre, degres=False)
  print("debug angle: ", angle)
  temps -= (distance(cylindre, roomba)/roomba.vitesse + abs(angle)/(2*roomba.vitesse))#Décompte du temps avant MAJ vitesse
  roomba.vitesse = vitesse(roomba.masse) #MAJ Vitesse avec nouvelle masse
  roomba.direction = np.array([cylindre.x - roomba.x, cylindre.y - roomba.y])
  roomba.x = cylindre.x #MAJ Position
  roomba.y = cylindre.y 
  print("nouvelle masse = ", roomba.masse," nouveau carburant = ", roomba.carburant," nouveau gain = ", round(collecte, 2)," temps restant = ", temps, "nouvelle vitesse = ", roomba.vitesse, "nouvelle position roomba : ",roomba.x, roomba.y)
  cylindre.isActive = False
  

def va(cylindre):
    sommeliens = 0
    for cylindresuiv in cylindre.connections:
        sommeliens += cylindresuiv.gain
    return sommeliens

def algo(roombatest, cylindres):
    global chemin
    global temps
    dirIni = np.array([0, 1])
    chemin = []
    while(temps>0 and roombatest.carburant>0): #Tant qu'il reste du temps et du carburant
        if(collecte == 0): #Si c'est la première itération
            print("debug : collecte = 0")
            mindist = math.inf 
            for cylindre in cylindres: #Pour tous les cylindres de la map
                tempdist = distance(cylindre, roombatest) - cylindre.gain*200 #calculer distance avec cylindre considéré
                print(tempdist)
                if tempdist < mindist:
                    print("maj mindist")
                    mindist = tempdist
                    cible = cylindre #maj cible
            collecter(cible, roombatest)
            chemin.append(cible.id)
        else:
            mincout = math.inf
            # isole = True
            for id_cylindre in cible.connections:
                if cylindres[id_cylindre].isActive:
                    isole = False
                    #tempsommeliens = -999
                    #sommeliens = va(cylindres[id_cylindre])
                    #if(sommeliens > tempsommeliens):
                        #tempsommeliens = sommeliens
                    if(roombatest.carburant > 1000):                                      
                        tempcout = distance(roombatest, cylindres[id_cylindre])/roombatest.vitesse+(100+3*roombatest.masse)*distance(roombatest, cylindres[id_cylindre])-cylindres[id_cylindre].gain*300 #Condition de choix... à améliorer 
                    else:
                        tempcout = (100+3*roombatest.masse)*distance(roombatest, cylindres[id_cylindre])  
                    if tempcout<mincout:
                        mincout = tempcout
                        cible = cylindres[id_cylindre]
                        solution = True
            # if isole:
            #     id_min = cible.connections[0]
            #     mincout = (100+3*roombatest.masse)*distance(roombatest, cylindres[cible.connections[0]])
            #     solution = roombatest.carburant > mincout
            #     if len(cible.connections) > 1:
            #         for id_cylindre in cible.connections:
            #             tempcout = roombatest.carburant > (100+3*roombatest.masse)*distance(roombatest, cylindres[id_cylindre])
            #             if roombatest.carburant > tempcout and tempcout < mincout:
            #                 mincout = tempcout
            #                 id_min = id_cylindre
            #                 solution = True
            #     if solution:
            #         cible = cylindres[id_min]
            #         print("bloqué", id_min)
            if(solution):
                if(roombatest.carburant - (100+3*roombatest.masse)*distance(cible, roombatest) > 0):
                    collecter(cible, roombatest)
                    chemin.append(cible.id)
                    for i in range(len(cylindres)):
                        cylindres[i].updateConnections(cylindres)
                else:
                    break
                solution = False
            else:
                print("plus de solutions!")
                break   
    if(temps<0):
        print("Temps écoulé!")
    elif(roombatest.carburant<0):
        print("Plus d'essence!")
    print("chemin = ", end='')
    if len(chemin) > 0:
        print(chemin[0], end='')
    if len(chemin) > 1:
        for id in chemin[1:]:
            print(' -> ' + str(id), end='')
        print()
    return chemin   
       
def main_algo():
    global collecte
    global temps
    sommep = 0
    roombatest = Roomba(0, 0)
    resultats = []
    cylindres = []
    # try:
    #     x, y, t = lireMap("donnees-map.txt")
    # except:
    #     x, y, t = lireMap("C:/Users/thund/OneDrive/Documents/chrobo/challenge_CHROBOT/donnees-map.txt")
    # for i in range(len(x)):
    #     cylindres.append(Cylindre(x[i], y[i], t[i]))
    #cylindres = genererRandomCylindres(nbCylindres=20, xmax=25, ymax=25, min_margin=3, printTxt=True)

    # for cylindre in cylindres:
    #     print(cylindre.id, cylindre.x, cylindre.y, cylindre.masse, cylindre.gain)
    # for i in range(len(cylindres)):
    #    cylindres[i].updateConnections(cylindres)
    #    sommep+=cylindres[i].gain
    temps = 300
    resultats = []
    collecte = 0
    # roombatest = Roomba(0, 0)
    # chemin = algo(roombatest, cylindres)
    for j in range(0,10):
        print("debug : passe numéro ",j)
        Cylindre.last_id = -1
        cylindres = genererRandomCylindres(nbCylindres=20, xmax=25, ymax=25, min_margin=3)
        for i in range(len(cylindres)):
            cylindres[i].updateConnections(cylindres)
            sommep+=cylindres[i].gain
        print("nb cylindres : ", len(cylindres))
        collecte = 0
        temps = 300
        roombatest = Roomba(0, 0)
        chemin = algo(roombatest, cylindres)
        print("gain = ", collecte,"/",sommep, "soit ",(collecte/sommep)*100,"%")
        resultats.append((collecte/sommep)*100)
        sommep = 0
    # print(resultats)
    print("------------------------------------------\n \n")
    print(sum(resultats)/len(resultats))
    # print("gain = ", collecte,"/",sommep, "soit ",(collecte/sommep)*100,"%")
    chemincyl = [cylindres[i] for i in chemin]
    res = planifie(chemincyl, Cylindre(0, 0, 1), np.array([1, 0]), printTxt = True)
    #simulate_turtle(res, quick=True)
    # afficherMap(cylindres, chemin, afficherTousLesIndices=False, gain=collecte, carburant=roombatest.carburant, temps=temps)
    

if __name__ == "__main__":
    main_algo()