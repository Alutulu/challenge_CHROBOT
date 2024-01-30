import numpy as np

def lireMap(filename):
    DataMap = np.loadtxt(filename, skiprows=0, dtype=float)
    #affichage des donnees de la carte
    x=DataMap[:,0]
    y=DataMap[:,1]
    t=DataMap[:,2]
    return x, y, t