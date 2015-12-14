import random
import math
import statistics
from tabulate import tabulate
from collections import OrderedDict

# Endogenise fitness (make relative) and population (restriction from resource constraints)
# Show: from low correlation to high correlation (inheritance)
# Show: from highest correlation to high correlation (inheritance)

class Element:
    def __init__(self, factors, fitness=None, correlation=None):
        low_start = True
        self.fitness = fitness if fitness != None else random.uniform(0.0,0.3 if low_start else 0.9)
        self.correlation = correlation if correlation != None else random.uniform(0.0 if low_start else 0.5,0.3 if low_start else 0.9)

    def __str__(self):
        return str(self.fitness)

def get_random_boolean(p):
    return random.random() < p

def reproduction(factors, population):

    def get_offspring(factors, parent):
        '''
        Core of model - establishes relationship between parent and offspring
        '''
        p_reproduce = parent.fitness if factors[0] == 0 else factors[0]
        if not get_random_boolean(p_reproduce):
            return []

        fitness_correlation = parent.correlation if factors[5] else random.random()
        correlation_correlation = parent.correlation if factors[6] else random.random()
        offspring = []

        for i in range(random.randint(0,factors[2])):
            fitness = factors[4](parent.fitness, fitness_correlation)
            correlation = factors[4](parent.correlation, correlation_correlation)
            offspring.append(Element(factors, fitness, correlation))
        return offspring

    return [x for y in population for x in get_offspring(factors, y)]

def selection(factors, population):
    return [x for x in population if get_random_boolean(x.fitness if factors[1] == 0 else factors[1])]

def get_population_summary(population, generation):
    fitness = [x.fitness for x in population]
    correlation = [x.correlation for x in population]
    ave_fitness = math.fsum(fitness)/len(population)
    ave_correlation = math.fsum(correlation)/len(population)

    if len(population) > 1:
        sd_fitness = statistics.stdev(fitness)
        sd_correlation = statistics.stdev(correlation)
    else:
        sd_fitness = sd_correlation = "NaN"

    summary = {'gen':generation, 'pop':len(population), 'ave_fit':ave_fitness, 'sd_fit':sd_fitness, 'ave_cor':ave_correlation, 'sd_cor':sd_correlation}
    return OrderedDict(sorted(summary.items(),key=lambda t: t[0])) # to guarantee ordering if we extract values later

def run(factors, population, generations, population_limit):

    original_population_size = len(population)
    population_limit *= original_population_size # stop when population size reaches a multiple of original population - generally some form of exponential growth

    # starting summary
    initial_summary = get_population_summary(population, 0)
    results = [initial_summary.keys()]

    for i in range(0,generations):

        parent_population = selection(factors, population)
        offspring_population = reproduction(factors, population)
        population = parent_population + offspring_population
        if factors[3] and len(population) > original_population_size: # if fixed population size
            population = random.sample(population, original_population_size)

        results.append(get_population_summary(population, i).values())

        if len(population) == 0 or len(population) > population_limit:
            break

    print(tabulate(results, headers="firstrow"))
    return (initial_summary, get_population_summary(population, i)) # (initial, final) results
