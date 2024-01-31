import tensorflow as tf
import numpy as np
from algo_basique import Roomba 
from main import calculeScore
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

#Paramètres
num_generations = 10
num_best = 5
output_size = 2
population_size = 50

class NeuralNet:
    def __init__(self, input_data, hidden, output_size):
        model = Sequential()
        self.input_size = input_data.shape[0] 
        model.add(Dense(self.input_size, activation='relu', input_shape(self.input_size,)))
        for hidden_size in hidden:
            model.add(Dense(hidden_size, activation='relu'))
        model.add(output_size, activation='softmax')
    
    def mutate(self, mutation_rate=0.01):
        #Mute le réseau de neurones
        weights = self.model.get_weights()
        new_weights = self.model.weights + mutation_rate * np.random.randn(*weights.shape)
        self.model.set_weights(new_weights)
    
    def evaluate(self, input_data):
        #Évalue le score du réseau
        pred = self.model.predict(input_data)
        return calculeScore(pred)

def crossover(p1, p2):
    #Fait le crossover entre deux parents
    point = np.random.randint(0, len(p1))
    child = np.concatenate((p1[:point], p2[point:]))
    return child

def neuroevolution(population_size, input_data, hidden = [64, 32], output_size):
    #Fonction qui simule la sélection naturelle
    population = [NeuralNet(input_data, hidden, output_size) for _ in range(population_size)]

    for generation in range(num_generations):
        scores = []
        for network in population:
            score = network.evaluate(input_data)
            scores.append(score)

        best_indices = np.argsort(scores)[-num_best:]
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
