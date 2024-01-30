from Cyclindre import Cylindre
from LireMap import lireMap
import numpy as np
from AfficherMap import afficherMap
from Planifie import planifie
from GenererMap import genererRandomCylindres

a = 6.98*10**(-2)
v0 = 1 
b0 = 100
b = 3
alpha = 10**(-1) 
qmax = 10000
tmax = 100
types = [
        (1, 1),
        (2, 2),
        (3, 2)
        ]

def distance(p1, p2):
    #Calcule la distance entre deux points
    return np.sqrt((p2.x-p1.x)**2 + (p2.y-p1.y)**2)

def vitesse(masse):
    #Calcule la vitesse du robot
    return v0*np.exp(-a*masse)

def calculeScore(posini, chemin):
    #Calcule le score de chaque chemin
    pos = posini 
    argent = 0
    masse = 0
    v = v0
    carburant = qmax 
    temps = 0
    n_cylindres = 0

    if(list(set(chemin)) != chemin):
        print("Attention ! Le chemin comporte des doublons")
        exit()

    for cylindre in chemin:
        dist = distance(pos, cylindre)
        carburant -= (b*masse + b0)*dist
        temps += dist/vitesse(masse)
        if(carburant < 0 or temps > tmax):
            print(f"Carburant restant : {carburant}, temps restant : {tmax-temps} secondes")
            print(f"Argent récolté : {argent}, Nombre de cylindres explorés : {n_cylindres}")
            return argent 
        else:
            n_cylindres += 1
            argent += cylindre.gain
            masse += cylindre.masse
            pos = cylindre
    print(f"Tous les cylindres ont été parcourus, carburant restant : {carburant}, temps restant : {tmax-temps} secondes")
    return argent

def main():
    cylindres = []
    try:
        x, y, t = lireMap("donnees-map.txt")
    except:
        x, y, t = lireMap("C:/Users/thund/OneDrive/Documents/chrobo/challenge_CHROBOT/donnees-map.txt")
    for i in range(len(x)):
        cylindres.append(Cylindre(x[i], y[i], t[i]))
    # Pour générer une map aléatoire :
    # cylindres = genererRandomCylindres(nbCylindres=20, xmax=25, ymax=25, min_margin=3)
    for i in range(len(cylindres)):
        cylindres[i].updateConnections(cylindres)
    n_cylindres = [2, 9, 5, 4, 3, 0]
    chemin = [cylindres[i] for i in n_cylindres] 
    posIni = Cylindre(0, 0, 1)
    dirIni = np.array([0, 1])
    res = planifie(chemin, posIni, dirIni)
    print(res)
    afficherMap(cylindres, n_cylindres, styleVirgile=False)

if __name__ == "__main__":
    main()
