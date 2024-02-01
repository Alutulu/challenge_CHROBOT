import numpy as np
from main import calculeScore, distance, vitesse, rotation
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from Cyclindre import Cylindre
from planifie import calculeAngle

#Paramètres
output_size = 2
population_size = 50

def hardmax(prediction):
    max_ind = np.argmax(prediction)
    res = np.zeros_like(predictions)
    res[max_ind] = 1

    return max_ind, res

class NeuralNet:
    def __init__(self, input_data, hidden, output_size, robot):
        model = Sequential()
        self.input_size = input_data.shape[0]
        self.robot = np.copy(robot)
        model.add(Dense(self.input_size, activation='relu', input_shape(self.input_size,)))
        for hidden_size in hidden:
            model.add(Dense(hidden_size, activation='relu'))
        model.add(Dense(output_size, activation='softmax'))
    
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
            pred = self.model.predict(data)
            id_pred, pred = hardmax(pred)
            cylindre = cylindres[id_pred]
            angle = calculeAngle(self.robot.direction, self.robot, cylindre)
            self.robot.temps -= angle/rotation(self.robot.masse)
            self.robot.direction = array([cylindre.x-robot.x, cylindre.y-robot.y]) 
            dist = distance(self.robot, cylindre)
            self.robot.x, self.robot.y = cylindre.x, cylindre.y
            self.robot.temps -= dist/vitesse(self.masse) 
            self.robot.gain += cylindre.gain
            self.robot.masse += cylidnre.masse
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
    data = []; extra = [robot.x, robot.y, robot.carburant, robot.vitesse, robot.masse, robot.direction, robot.temps]
    for i, cylindre in enumerate(cylindres):
        if i in explored:
            data.append(-1000)
        else:
            data.append(distance(robot, cylindre))            
    data += extra
    return np.array(data)

def neuroevolution(population_size, input_data, hidden = [64, 32], output_size, robot, n_generations = 10, n_elite = 5):
    #Fonction qui simule la sélection naturelle
    population = [NeuralNet(input_data, hidden, output_size, robot) for _ in range(population_size)]

    for generation in range(n_generations):
        scores = []
        for network in population:
            score = network.evaluate(input_data)
            scores.append(score)

        best_indices = np.argsort(scores)[-n_elite:]
        bests = [population[i] for i in best_indices]

        new_population = bests.copy()
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

cylindres = []
try:
    x, y, t = lireMap("donnees-map.txt")
except:
    x, y, t = lireMap("C:/Users/thund/OneDrive/Documents/chrobo/challenge_CHROBOT/donnees-map.txt")
for i in range(len(x)):
    cylindres.append(Cylindre(x[i], y[i], t[i]))

robot = Roomba(0, 0, masse = 0)
init_data = update_data(robot, cylindres)
meilleur = neuroevolution(population_size = 50, data, hidden = [20, 20], len(cylindres), robot, n_generations = 10, n_elite = 5)
