import numpy as np
import matplotlib.pyplot as plt
import math

def afficherMap(listCylindres, chemin=None, afficherTousLesIndices=False, styleVirgile=False):
    # le chemin doit être une liste des indices de cylindre (int)
    tColorTab = {1:'y', 2:'c', 3:'m'}
    dbRayon = 1

    fig = plt.figure(1)
    fig.set_figheight(7)
    ax = fig.gca()
    ax.set_aspect('equal', adjustable='box')
    for cylindre in listCylindres:
        if chemin != None:
           if cylindre.id in chemin:
              numero = chemin.index(cylindre.id)
              c2 = plt.Circle((cylindre.x+1,cylindre.y+1), 0.4,color='w', zorder=4.0)
              plt.text(cylindre.x+1, cylindre.y+1, chr(ord('A') + numero), fontsize='medium', zorder=5.0, color='r')
              ax.add_patch(c2)
        c1 = plt.Circle((cylindre.x,cylindre.y), dbRayon,color=tColorTab[int(cylindre.type)] )
        plt.text(cylindre.x-0.55, cylindre.y+0.2, str(cylindre.masse) + "kg", fontsize='medium')
        plt.text(cylindre.x-0.4, cylindre.y-0.6, str(cylindre.gain) + "€", fontsize='medium')
        ax.add_patch(c1)
        # affiche l'indice de tous les cylindres
        if afficherTousLesIndices:
          c3 = plt.Circle((cylindre.x+1,cylindre.y-1), 0.4,color='w', zorder=4.0)
          plt.text(cylindre.x+1, cylindre.y-1, str(cylindre.id), fontsize='medium', zorder=5.0, color='b')
          ax.add_patch(c3)

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
              plt.plot((new_x1, new_x2), (new_y1, new_y2), color=color, linestyle='-', linewidth=1.0, zorder=1.0)
            else:
              plt.plot((new_x1, new_x2), (new_y1, new_y2), color='k', linestyle='--', linewidth=1.0, zorder=1.0)
            middle = (x1 + vector[0] / 2, y1 + vector[1] / 2)
            size_background = 0.4 if len(str(round(norm, 1))) <= 3 else 0.55
            c1 = plt.Circle((middle[0],middle[1]), size_background,color='w', zorder=2.0)
            ax.add_patch(c1)
            offset_x = 0.4 if len(str(round(norm, 1))) <= 3 else 0.65
            plt.text(middle[0]-offset_x, middle[1]-0.2, str(round(norm, 1)), fontsize='small', zorder=3.0)

    plt.show()