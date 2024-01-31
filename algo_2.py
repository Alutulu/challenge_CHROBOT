import tensorflow as tf
import numpy as np
from algo_basique import Roomba 
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

#Paramètres
num_generations = 10
num_best = 5
input_size = 8
output_size = 2
population_size = 50

class NeuralNet:
    def __init__(self, input_size, output_size):
        model = Sequential()
        model.add(Dense(64, activation='relu', input_shape=(input_size,)))
        model.add(Dense(64, activation='relu'))
        model.add(output_size, activation='softmax')
    
    def mutate(self, mutation_rate=0.01):
        #Mute le réseau de neurones
        weights = self.get_weights()
        new_weights = self.weights + mutation_rate * np.random.randn(*weights.shape)
        self.set_weights(new_weights)

def crossover(p1, p2):
    point = np.random.randint(0, len(p1))
    child = np.concatenate((p1[:point], p2[point:]))
    return child

def neuroevolution(population_size, input_size, output_size):
    population = [NeuralNet(input_size, output_size) for _ in range(population_size)]

    for generation in num_generations:
        scores = []
        for network in population:
            score = network.evaluate()
            scores.append(score)

        best_indices = np.argsort(scores)[-num_best:]
        bests = [population[i] for i in best_indices]

        new_population = bests.copy()
        while len(new_population) < population_size:
            p1 = np.random.choice(bests)
            p2 = np.random.choice(bests)
            child_weights = crossover(p1.get_weights(), p2.get_weights())
            child = NeuralNet()
