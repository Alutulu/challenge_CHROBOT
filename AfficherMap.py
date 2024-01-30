import numpy as np
import matplotlib.pyplot as plt
import math

def afficherMap(listCylindres, styleVirgile = False):
    tColorTab = {1:'green', 2:'blue', 3:'red'}
    dbRayon = 1

    x = [cylindre.x for cylindre in listCylindres]
    y = [cylindre.y for cylindre in listCylindres]
    t = [cylindre.type for cylindre in listCylindres]

    n = len(x)
    fig = plt.figure(1)
    ax = fig.gca()
    for i in range(n):
        plt.plot(x[i],y[i],marker='+',color=tColorTab[int(t[i])])
        c1 = plt.Circle((x[i],y[i]), dbRayon,color=tColorTab[int(t[i])] )
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