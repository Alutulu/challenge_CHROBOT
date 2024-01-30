import numpy as np
import matplotlib.pyplot as plt
import math

def afficherMap(listCylindres, styleVirgile = False):
    tColorTab = {1:'green', 2:'blue', 3:'red'}
    dbRayon = 1

    fig = plt.figure(1)
    fig.set_figheight(7)
    ax = fig.gca()
    ax.set_aspect('equal', adjustable='box')
    for cylindre in listCylindres:
        c1 = plt.Circle((cylindre.x,cylindre.y), dbRayon,color=tColorTab[int(cylindre.type)] )
        plt.text(cylindre.x-0.55, cylindre.y+0.2, str(cylindre.masse) + "kg", fontsize='medium')
        plt.text(cylindre.x-0.4, cylindre.y-0.6, str(cylindre.gain) + "€", fontsize='medium')
        ax.add_patch(c1)

    colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
    for i in range(len(listCylindres)):
      cylindreDep = listCylindres[i]
      color = colors[i%len(colors)]
      for j in cylindreDep.connections:
         if j > i:
            cylindreDest = listCylindres[j]
            x1, y1, x2, y2 = cylindreDep.x, cylindreDep.y, cylindreDest.x, cylindreDest.y
            vector = (x2-x1, y2-y1)
            norm = math.sqrt(vector[0]**2 + vector[1]**2)
            vector_normalized = (vector[0] / norm, vector[1] / norm)
            new_x1, new_x2, new_y1, new_y2 = cylindreDep.x + vector_normalized[0] * 1.1, cylindreDest.x - vector_normalized[0] * 1.1, cylindreDep.y + vector_normalized[1] * 1.1, cylindreDest.y - vector_normalized[1] * 1.1
            if styleVirgile:
              plt.plot((new_x1, new_x2), (new_y1, new_y2), color=color, linestyle='-', linewidth=1.0)
            else:
              plt.plot((new_x1, new_x2), (new_y1, new_y2), color='k', linestyle='--', linewidth=1.0)

    plt.show()