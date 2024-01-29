from Cyclindre import Cylindre
from LireMap import lireMap

def main():
    cylindres = []
    x, y, t = lireMap("C:/Users/thund/OneDrive/Documents/chrobo/challenge_CHROBOT/donnees-map.txt", afficherMap=False)
    for i in range(len(x)):
        cylindres.append(Cylindre(x[i], y[i], t[i]))
    for cylindre in cylindres:
        print(cylindre.id, cylindre.x, cylindre.y, cylindre.masse, cylindre.gain)
    for i in range(len(cylindres)):
        cylindres[i].updateConnections(cylindres)
    print(cylindres[0].connections)

if __name__ == "__main__":
    main()