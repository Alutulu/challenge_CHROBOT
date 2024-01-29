# utilitaire permettant de charger les donnees de la carte du
# challenge et de la visualiser
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

def lireMap(filename = None, afficherMap = True):
    tColorTab = {1:'red', 2:'green', 3:'blue'}
    dbRayon = 0.85
    nom_fichier = ""
    ##########################
    # point d'entree du script 
    ##########################
    argc = len(sys.argv)
    if argc < 2 and filename == None:
        print("preciser le nom du fichier de donnees en argument...")
        exit()
    if filename == None:
        nom_fichier = sys.argv[1]
    else:
        nom_fichier = filename
    #lecture du fichier
    DataMap = np.loadtxt(nom_fichier, skiprows=1, dtype=float)
    #affichage des donnees de la carte
    x=DataMap[:,0]
    y=DataMap[:,1]
    t=DataMap[:,2]
    if afficherMap:
        n = len(x)
        fig = plt.figure(1)
        ax = fig.gca()
        for i in range(n):
            plt.plot(x[i],y[i],marker='+',color=tColorTab[int(t[i])])
            c1 = plt.Circle((x[i],y[i]), dbRayon,color=tColorTab[int(t[i])] )
            ax.add_patch(c1)
        plt.show()
    return x, y, t