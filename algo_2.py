import numpy as np
from main import calculeScore, distance, vitesse, rotation
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

    def copy(self):
        #Copie le roomba
        return Roomba(self.x, self.y, self.rayon, self.carburant, self.vitesse, self.masse)
    
    def calculeVitesse(self) -> float:
        return v0*np.exp(-a*self.masse)
    
    def distanceCylindre(self, cyl) -> float:
        return distance(self, cyl)

def hardmax(prediction):
    print(f'prediction : {prediction}')
    max_ind = np.argmax(prediction)
    print(max_ind)
    res = np.zeros_like(prediction)
    res[max_ind] = 1

    return max_ind, res

class NeuralNet:
    def __init__(self, input_data, hidden, output_size, robot):
        self.model = Sequential()
        self.input_size = input_data.shape[1]
        self.robot = robot.copy()
        self.model.add(InputLayer(input_shape = (self.input_size, 1)))
        for hidden_size in hidden:
            self.model.add(Dense(hidden_size, activation='relu'))
        self.model.add(Dense(output_size, activation='linear'))
        #self.model.summary()
    
    def mutate(self, mutation_rate=0.01):
        #Mute le réseau de neurones
        weights = self.model.get_weights()
        new_weights = self.model.weights + mutation_rate * np.random.randn(*weights.shape)
        self.model.set_weights(new_weights)
    
    def evaluate(self, input_data):
        #Simule le parcours du robot
        chemin = []
        data = input_data
        
        while(self.robot.carburant > 0 and self.robot.temps > 0):
            print(f'data : {data}')
            pred = self.model.predict(data)
            print(f'prediction : {pred}')
            id_pred, pred = hardmax(pred)
            cylindre = cylindres[id_pred]
            angle = calculeAngle(self.robot.direction, self.robot, cylindre)
            self.robot.temps -= angle/rotation(self.robot.masse)
            self.robot.direction = array([cylindre.x-robot.x, cylindre.y-robot.y]) 
            dist = self.robot.calculeDistance(cylindre)
            self.robot.x, self.robot.y = cylindre.x, cylindre.y
            self.robot.temps -= dist/vitesse(self.masse) 
            self.robot.vitesse = self.robot.calculeVitesse()
            self.robot.gain += cylindre.gain
            self.robot.masse += cylindre.masse
            chemin.append(cylindre)
            data = update_data(self.robot, cylindres, chemin)

        return self.robot.gain

def crossover(p1, p2):
    #Fait le crossover entre deux parents
    point = np.random.randint(0, len(p1))
    child = np.concatenate((p1[:point], p2[point:]))
    return child


def update_data(robot, cylindres, explored = []):
    #Renvoie le vecteur data initial (voir pour ajouter du temps)
    data = []; extra = [robot.x, robot.y, robot.carburant, robot.vitesse, robot.masse, robot.direction[0], robot.direction[1], robot.temps]
    for i, cylindre in enumerate(cylindres):
        if i in explored:
            data.append(-1000)
        else:
            data.append(distance(robot, cylindre))            
    data += extra
    data = np.array(data)
    return data.reshape(1, 28)

def neuroevolution(population_size, input_data, hidden, output_size, robot, n_generations = 10, n_elite = 5):
    #Fonction qui simule la sélection naturelle
    population = [NeuralNet(input_data, hidden, output_size, robot) for _ in range(population_size)]

    for generation in range(n_generations):
        scores = []
        for network in population:
            score = network.evaluate(input_data)
            scores.append(score)

        best_indices = np.argsort(scores)[-n_elite:]
        bests = [population[i] for i in best_indices]

        new_population = bests[:]
        while len(new_population) < population_size:
            p1 = np.random.choice(bests)
            p2 = np.random.choice(bests)
            child_weights = crossover(p1.get_weights(), p2.get_weights())
            child = NeuralNet(input_data, hidden, output_size)
            child.model.set_weights(child_weights)
            new_population.append(child)

        population = new_population
    best_network = bests[0]
    return best_network
