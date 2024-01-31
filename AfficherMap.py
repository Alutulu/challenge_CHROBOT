import numpy as np
import matplotlib.pyplot as plt
import math
from Cyclindre import Cylindre

def afficherMap(listCylindres, chemin=None, gain=None, carburant=None, temps=None, afficherTousLesIndices=False, styleVirgile=False):
    # le chemin doit être une liste des indices de cylindre (int)
    tColorTab = {1:'#FEFFB2', 2:'#FFD6B2', 3:'#FFB2CB'}
    dbRayon = 1

    fig_global, (fig, legende) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 2]})
    fig_global.suptitle("Graphe tournée")
    manager = plt.get_current_fig_manager()
    try:
      manager.window.showMaximized()
    except:
      fig_global.set_figwidth(100)
      fig_global.set_figheight(100)
    fig.set_aspect('equal')
    for cylindre in listCylindres:
        if chemin != None:
           if cylindre.id in chemin:
              numero = chemin.index(cylindre.id)
              fig.text(cylindre.x-0.22, cylindre.y-0.18, chr(ord('A') + numero), fontsize='medium', zorder=5.0, color='r')
        c1 = plt.Circle((cylindre.x,cylindre.y), dbRayon,color=tColorTab[int(cylindre.type)])
        fig.add_patch(c1)
        if chemin != None:
           if cylindre.id in chemin:
                c1 = plt.Circle((cylindre.x,cylindre.y), dbRayon+0.05,color='r', fill=False)
        fig.add_patch(c1)

        # Affiche l'indice de tous les cylindres
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
            vector_perp = (-vector_normalized[1], vector_normalized[0])
            new_x1, new_x2, new_y1, new_y2 = cylindreDep.x + vector_normalized[0] * 1.1, cylindreDest.x - vector_normalized[0] * 1.1, cylindreDep.y + vector_normalized[1] * 1.1, cylindreDest.y - vector_normalized[1] * 1.1
            flecheArrivee = None # True si la fleche est sur le cylindre d'indice j, False si indice i, et None si pas de chemin donné en paramètre
            if chemin != None:
              cheminTraverse = False
              for id in range((len(chemin)-1)):
                id_cylindre_dep = chemin[id]
                id_cylindre_dest = chemin[id+1]
                if id_cylindre_dep == i and id_cylindre_dest == j:
                    cheminTraverse = True
                    flecheArrivee = True
                    break
                elif id_cylindre_dep == j and id_cylindre_dest == i:
                   cheminTraverse = True
                   flecheArrivee = False
                   break
              couleurChemin = 'k' if not cheminTraverse else 'r'
              styleChemin = '--' if not cheminTraverse else '-'
              sizeChemin = 0.5 if not cheminTraverse else 1.2
            else:
               couleurChemin = 'k'
               styleChemin = '--'
               sizeChemin = 0.5
            fig.plot((new_x1, new_x2), (new_y1, new_y2), color=couleurChemin, linestyle=styleChemin, linewidth=sizeChemin, zorder=1.0)
            if flecheArrivee == True:
              fig.plot((new_x2, new_x2 + 0.3*(vector_perp[0] - vector_normalized[0])), (new_y2, new_y2 + 0.3*(vector_perp[1] - vector_normalized[1])), color=couleurChemin, linestyle=styleChemin, linewidth=sizeChemin, zorder=1.0)
              fig.plot((new_x2, new_x2 + 0.3*(-vector_perp[0] - vector_normalized[0])), (new_y2, new_y2 + 0.3*(-vector_perp[1] - vector_normalized[1])), color=couleurChemin, linestyle=styleChemin, linewidth=sizeChemin, zorder=1.0)
            elif flecheArrivee == False:
              fig.plot((new_x1, new_x1 + 0.3*(vector_perp[0] + vector_normalized[0])), (new_y1, new_y1 + 0.3*(vector_perp[1] + vector_normalized[1])), color=couleurChemin, linestyle=styleChemin, linewidth=sizeChemin, zorder=1.0)
              fig.plot((new_x1, new_x1 + 0.3*(-vector_perp[0] + vector_normalized[0])), (new_y1, new_y1 + 0.3*(-vector_perp[1] + vector_normalized[1])), color=couleurChemin, linestyle=styleChemin, linewidth=sizeChemin, zorder=1.0)
            middle = (x1 + vector[0] / 2, y1 + vector[1] / 2)
            size_background = 0.4 if len(str(round(norm, 1))) <= 3 else 0.6
            c1 = plt.Circle((middle[0],middle[1]), size_background,color='w', zorder=2.0)
            fig.add_patch(c1)
            offset_x = 0.4 if len(str(round(norm, 1))) <= 3 else 0.65
            fig.text(middle[0]-offset_x, middle[1]-0.2, str(round(norm, 1)), fontsize='x-small', zorder=3.0, color=couleurChemin)

    # Légende
    legende.set_aspect('equal')
    y_circle = (0.9, 0.75, 0.6)
    for i in range(3):
      c1 = plt.Circle((0.15, y_circle[i]), 0.05, color=tColorTab[i+1])
      legende.add_patch(c1)
      legende.text(0.25, y_circle[i]+0.02, "Masse : " + str(Cylindre.type_param[i+1]['masse']) + 'kg', fontsize='large')
      legende.text(0.25, y_circle[i]-0.04, "Gain : " + str(Cylindre.type_param[i+1]['gain']) + '€', fontsize='large')
    legende.get_xaxis().set_visible(False)
    legende.get_yaxis().set_visible(False)
    legende.spines['top'].set_visible(False)
    legende.spines['right'].set_visible(False)
    legende.spines['bottom'].set_visible(False)
    legende.spines['left'].set_visible(False)
    if gain != None:
      legende.text(0.0, 0.3, "Gain final : " + str(gain) + " €", fontsize='xx-large')
    if carburant != None:
      legende.text(0.0, 0.2, "Carburant restant : " + str(round(carburant, 2)) + " L", fontsize='xx-large')
    if temps != None:
      legende.text(0.0, 0.1, "Temps restant : " + str(round(temps, 2)) + " s", fontsize='xx-large')

    plt.show()