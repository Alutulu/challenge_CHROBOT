from Cyclindre import Cylindre
from numpy.linalg import norm
from numpy import sqrt, cos, sin, arctan2, array, degrees, cross, dot

def planifie(chemin, posIni, dirIni, printTxt = False):
    """Planifie le chemin du robot
       :param list chemin: Chemin (liste de Cylindres)
       :param Cylindre posIni: Position initiale du robot
       :param Array dirIni: Direction initiale du robot
       :param boolean printTxt: True si tu veux sauvegarder en txt
       """
    primitives = []
    direction = array(dirIni)
    position = posIni

    for etape in chemin:
        vec = array([etape.x-position.x, etape.y-position.y]) 
        rad = arctan2(cross(direction, vec), dot(direction, vec))
        deg = degrees(rad)
        dist = sqrt((position.x-etape.x)**2 + (position.y-etape.y)**2)
        primitives.append(f'Turn {deg}')
        primitives.append(f'Go {dist}')
        direction = vec  
        position = etape

    if(printTxt):
        with open('instructions.txt', 'w') as file:
            for ligne in primitives:
                file.writelines(ligne + '\n')
    else:
        return primitives
