import numpy as np
from main import calculeScore, distance, vitesse, rotation, v0, a, b0, b, alpha
from tensorflow.keras.layers import Dense, InputLayer
from tensorflow.keras.models import Sequential
from Cyclindre import Cylindre
from Planifie import calculeAngle

#Paramètres
population_size = 50
temps = 300

class Roomba:
    def __init__(self, x, y, rayon = 1, carburant = 10000, vitesse = 1, masse = 1):
        self.x = x
        self.y = y
        self.rayon = rayon
        self.carburant = carburant
        self.vitesse = vitesse
        self.masse = masse
        self.direction = np.array([1, 0])
        self.temps = temps
        self.gain = 0
        self.explored = []

    def copy(self):
        #Copie le roomba
        return Roomba(self.x, self.y, self.rayon, self.carburant, self.vitesse, self.masse)
    
    def calculeVitesse(self) -> float:
        return v0*np.exp(-a*self.masse)
    
    def calculeDistance(self, cyl) -> float:
        return distance(self, cyl)

    def calculeCarburant(self, dist) -> float:
        return (b*self.masse + b0)*dist

def hardmax(prediction):
    max_ind = np.argmax(prediction)
    res = np.zeros_like(prediction)
    res[0][max_ind] = 1

    return max_ind, res

class NeuralNet:
    def __init__(self, input_data, hidden, output_size, robot):
        self.model = Sequential()
        self.input_size = input_data.shape[1]
        self.robot = robot.copy()
        self.model.add(InputLayer(input_shape = (1, self.input_size)))
        for hidden_size in hidden:
            self.model.add(Dense(hidden_size, activation='relu'))
        self.model.add(Dense(output_size, activation='softmax'))
        #self.model.summary()
    
    def mutate(self, mutation_rate=0.01):
        # Mute le réseau de neurones
        weights = self.model.get_weights()
        new_weights = [w + mutation_rate * np.random.randn(*w.shape) for w in weights]
        self.model.set_weights(new_weights)

    def evaluate(self, input_data, cylindres):
        #Simule le parcours du robot
        data = input_data
        
        while(self.robot.carburant > 0 and self.robot.temps > 0):
            pred = self.model.predict(np.expand_dims(data, axis=0), verbose=0)[0]
            id_pred, pred = hardmax(pred)
            cylindre = cylindres[id_pred]
            angle = calculeAngle(self.robot.direction, self.robot, cylindre)
            self.robot.temps -= angle/rotation(self.robot.masse)
            self.robot.direction = np.array([cylindre.x-self.robot.x, cylindre.y-self.robot.y]) 
            dist = self.robot.calculeDistance(cylindre)
            if cylindre not in self.robot.explored:
                self.robot.x, self.robot.y = cylindre.x, cylindre.y
                self.robot.temps -= dist/vitesse(self.robot.masse) 
                self.robot.vitesse = self.robot.calculeVitesse()
                self.robot.carburant -= self.robot.calculeCarburant(dist)
                self.robot.gain += cylindre.gain
                self.robot.masse += cylindre.masse
                data = update_data(self.robot, cylindres)
                self.robot.explored.append(cylindre)
            self.robot.temps -= 2

        return self.robot.gain

def crossover(p1, p2):
    # Fait le crossover entre deux parents
    child_weights = []
    for w1, w2 in zip(p1.model.get_weights(), p2.model.get_weights()):
        point = np.random.randint(0, len(w1.flatten()))
        child = np.concatenate((w1.flatten()[:point], w2.flatten()[point:]))
        child_weights.append(child.reshape(w1.shape))

    return child_weights


def update_data(robot, cylindres):
    #Renvoie le vecteur data initial (voir pour ajouter du temps)
    data = []; extra = [robot.x, robot.y, robot.carburant, robot.vitesse, robot.masse, robot.direction[0], robot.direction[1], robot.temps]
    for i, cylindre in enumerate(cylindres):
        if cylindre in robot.explored:
            data.append(-1000)
        else:
            data.append(distance(robot, cylindre))            
    data += extra
    data = np.array(data)
    return data.reshape(1, 28)

def neuroevolution(population_size, input_data, hidden, cylindres, robot, n_generations = 10, n_elite = 5):
    #Fonction qui simule la sélection naturelle
    output_size = len(cylindres)
    population = [NeuralNet(input_data, hidden, output_size, robot) for _ in range(population_size)]

    for generation in range(n_generations):
        scores = []
        for network in population:
            score = network.evaluate(input_data, cylindres)
            scores.append(score)
            print(f"Robot évalué, score : {score}, carburant restant : {network.robot.carburant}, temps restant : {network.robot.temps}")

        best_indices = np.argsort(scores)[-n_elite:]
        bests = [population[i] for i in best_indices]
        best_scores = [nn.robot.gain for nn in bests]
        print(f'Génération {generation} : meilleurs scores : {best_scores}')

        new_population = bests[:]
        while len(new_population) < population_size:
            p1 = np.random.choice(bests)
            p2 = np.random.choice(bests)
            child_weights = crossover(p1, p2)
            child = NeuralNet(input_data, hidden, output_size, robot)
            child.model.set_weights(child_weights)
            new_population.append(child)

        population = new_population
    best_network = bests[0]
    return best_network
