import random
import math
import statistics
#from tabulate import tabulate
from collections import OrderedDict

# Endogenise fitness (make relative) and population (restriction from resource constraints)
# Show: from low fidelity to high fidelity (inheritance)
# Show: from highest fidelity to high fidelity (inheritance)


class Element:
    def __init__(self, fitness=None, fidelity=None, low_start = True):
        '''low_start only relevant if fitness or fidelity not provided'''

        if fitness is not None:
            self.fitness = fitness
        else:
            self.fitness = random.uniform(0.0, 0.3 if low_start else 0.9)
        if fidelity is not None:
            self.fidelity = fidelity
        else:
            self.fidelity = random.uniform(0.0 if low_start else 0.5, 0.3 if low_start else 0.9)

    def __str__(self):
        return str(self.fitness)


def get_random_boolean(p):
    return random.random() < p


def reproduction(factors, population):

    def derive(source, correlation):
        x = random.gauss(source, 1.0 - correlation)
        while x < 0.0 or x > 1.0:
            x = random.gauss(source, 1.0 - correlation)
        assert 1.0 >= x >= 0.0
        return x

    def get_offspring(factors, parent):
        '''
        Core of model - establishes relationship between parent and offspring
        '''

        p_reproduce = parent.fitness if factors['P_REPRODUCE'] == 0 else factors['P_REPRODUCE']
        if not get_random_boolean(p_reproduce):
            return []

        fidelity_fidelity = parent.fidelity if factors['CORRELATED'] else random.random()
        offspring = []

        for i in range(random.randint(0, factors['N_OFFSPRING'])):
            fitness = derive(parent.fitness, parent.fidelity)
            fidelity = derive(parent.fidelity, fidelity_fidelity)
            offspring.append(Element(fitness, fidelity))
        return offspring

    return [x for y in population for x in get_offspring(factors, y)]


def selection(factors, population):
    return [x for x in population if get_random_boolean(x.fitness if factors['P_SELECTION'] == 0 else factors['P_SELECTION'])]


def apply_environment_change(t, environment, population):

    def adjust_fitness(fitness, environment_change):
        bucket = math.floor(fitness*len(environment_change)) - 1  # bucket number is floor(x/bucket_size)
        if bucket < 0:  # adjust as fitness values of 0 and 1 are both possible, so either top or bottom bucket adjusted
            bucket = 0
        return environment_change[bucket]

    wrapped_t = t % len(environment)  # environment has a period, so must wrap t
    return [Element(adjust_fitness(x.fitness, environment[wrapped_t]), x.fidelity) for x in population]


def get_population_summary(population, generation):
    fitness = [x.fitness for x in population]
    fidelity = [x.fidelity for x in population]

    if len(population) > 1:
        sd_fitness = statistics.stdev(fitness)
        sd_fidelity = statistics.stdev(fidelity)
    else:
        sd_fitness = sd_fidelity = "NaN"

    if len(population) > 0:
        ave_fitness = math.fsum(fitness)/len(population)
        ave_fidelity = math.fsum(fidelity)/len(population)
    else:
        ave_fitness = ave_fidelity = "NaN"

    summary = {'gen': generation,
               'pop': len(population),
               'ave_fit': ave_fitness,
               'sd_fit': sd_fitness,
               'ave_cor': ave_fidelity,
               'sd_cor': sd_fidelity}

    return OrderedDict(sorted(summary.items(), key=lambda t: t[0]))  # to guarantee ordering if we extract values later


def run(factors, population, generations, population_limit, environment):

    original_population_size = len(population)
    population_limit *= original_population_size # stop when population size reaches a multiple of original population - generally some form of exponential growth

    # starting summary
    initial_summary = get_population_summary(population, 0)
    results = [initial_summary] # headers and starting conditions

    for t in range(1, generations+1):

        parent_population = selection(factors, population)
        offspring_population = reproduction(factors, population)
        population = parent_population + offspring_population

        if len(population) > original_population_size:  # if fixed population size
            population = random.sample(population, original_population_size)
        if len(population) < 3 or len(population) > population_limit:
            break

        results.append(get_population_summary(population, t))

        population = apply_environment_change(t, environment, population)

    #print(tabulate([x.values() for x in results], headers=results[0].keys()))
    return results
