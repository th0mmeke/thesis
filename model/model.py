import random
import math
import statistics
from tabulate import tabulate
from collections import OrderedDict

# Endogenise fitness (make relative) and population (restriction from resource constraints)
# Show: from low correlation to high correlation (inheritance)
# Show: from highest correlation to high correlation (inheritance)

class Element:
    def __init__(self, fitness=None, correlation=None, low_start = True):
        '''low_start only relevant if fitness or correlation not provided'''
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
            offspring.append(Element(fitness, correlation))
        return offspring

    return [x for y in population for x in get_offspring(factors, y)]

def selection(factors, population):
    return [x for x in population if get_random_boolean(x.fitness if factors[1] == 0 else factors[1])]

def tweak_fitness(factors, population, correlation=0.95):
    return [Element(factors[4](x.fitness-0.2, correlation), x.correlation) for x in population]

def get_population_summary(population, generation):
    fitness = [x.fitness for x in population]
    correlation = [x.correlation for x in population]

    if len(population) > 1:
        sd_fitness = statistics.stdev(fitness)
        sd_correlation = statistics.stdev(correlation)
    else:
        sd_fitness = sd_correlation = "NaN"

    if len(population) > 0:
        ave_fitness = math.fsum(fitness)/len(population)
        ave_correlation = math.fsum(correlation)/len(population)
    else:
        ave_fitness = ave_correlation = "NaN"

    summary = {'gen':generation, 'pop':len(population), 'ave_fit':ave_fitness, 'sd_fit':sd_fitness, 'ave_cor':ave_correlation, 'sd_cor':sd_correlation}
    return OrderedDict(sorted(summary.items(),key=lambda t: t[0])) # to guarantee ordering if we extract values later

def run(factors, population, generations, population_limit, environment_change_frequency):

    original_population_size = len(population)
    population_limit *= original_population_size # stop when population size reaches a multiple of original population - generally some form of exponential growth

    # starting summary
    initial_summary = get_population_summary(population, 0)
    results = [initial_summary] # headers and starting conditions

    for i in range(1,generations+1):

        parent_population = selection(factors, population)
        offspring_population = reproduction(factors, population)
        population = parent_population + offspring_population
        if len(population) > original_population_size: # if fixed population size
            if factors[3]:
                sorted_population = sorted(population, key=lambda element: element.fitness, reverse=True)
                population = sorted_population[0:original_population_size]
            else:
                population = random.sample(population, original_population_size)

        if len(population) < 3 or len(population) > population_limit:
            break

        results.append(get_population_summary(population, i))

        if environment_change_frequency > 0 and i % environment_change_frequency == 0:
            population = tweak_fitness(factors, population, 0.70)

    #print(tabulate([x.values() for x in results], headers=results[0].keys()))
    return results
