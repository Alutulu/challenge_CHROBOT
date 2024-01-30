import numpy as np
import matplotlib.pyplot as plt
import math

def afficherMap(listCylindres, chemin=None, afficherTousLesIndices=False, styleVirgile=False):
    # le chemin doit être une liste des indices de cylindre (int)
    tColorTab = {1:'y', 2:'c', 3:'m'}
    dbRayon = 1

    fig_global, (fig, legende) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]})
    fig_global.suptitle("Graphe tournée")
    fig_global.set_figwidth(50)
    fig_global.set_figheight(50)
    fig.set_aspect('equal')
    for cylindre in listCylindres:
        if chemin != None:
           if cylindre.id in chemin:
              numero = chemin.index(cylindre.id)
              c2 = plt.Circle((cylindre.x+1,cylindre.y+1), 0.4,color='w', zorder=4.0)
              fig.text(cylindre.x+1, cylindre.y+1, chr(ord('A') + numero), fontsize='medium', zorder=5.0, color='r')
              fig.add_patch(c2)
        c1 = plt.Circle((cylindre.x,cylindre.y), dbRayon,color=tColorTab[int(cylindre.type)])
        fig.text(cylindre.x-0.55, cylindre.y+0.2, str(cylindre.masse) + "kg", fontsize='medium')
        fig.text(cylindre.x-0.4, cylindre.y-0.6, str(cylindre.gain) + "€", fontsize='medium')
        fig.add_patch(c1)
        # affiche l'indice de tous les cylindres
        if afficherTousLesIndices:
          c3 = plt.Circle((cylindre.x+1,cylindre.y-1), 0.4,color='w', zorder=4.0)
          fig.text(cylindre.x+1, cylindre.y-1, str(cylindre.id), fontsize='medium', zorder=5.0, color='b')
          fig.add_patch(c3)

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
              fig.plot((new_x1, new_x2), (new_y1, new_y2), color=color, linestyle='-', linewidth=1.0, zorder=1.0)
            else:
              fig.plot((new_x1, new_x2), (new_y1, new_y2), color='k', linestyle='--', linewidth=1.0, zorder=1.0)
            middle = (x1 + vector[0] / 2, y1 + vector[1] / 2)
            size_background = 0.4 if len(str(round(norm, 1))) <= 3 else 0.55
            c1 = plt.Circle((middle[0],middle[1]), size_background,color='w', zorder=2.0)
            fig.add_patch(c1)
            offset_x = 0.4 if len(str(round(norm, 1))) <= 3 else 0.65
            fig.text(middle[0]-offset_x, middle[1]-0.2, str(round(norm, 1)), fontsize='small', zorder=3.0)

    # Légende
    legende.set_aspect('equal')
    c1 = plt.Circle((0.15, 0.75), 0.05, color=tColorTab[1])
    legende.add_patch(c1)
    c1 = plt.Circle((0.15, 0.5), 0.05, color=tColorTab[2])
    legende.add_patch(c1)
    c1 = plt.Circle((0.15, 0.25), 0.05, color=tColorTab[3])
    legende.add_patch(c1)
    legende.get_xaxis().set_visible(False)
    legende.get_yaxis().set_visible(False)

    plt.show()