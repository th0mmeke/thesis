import random
import math
import statistics
from collections import OrderedDict


class Element:

    def __init__(self, lineage, fitness=None, fidelity=None):
        if fitness is None:
            fitness = random.uniform(0.0, 0.3)
        if fidelity is None:
            fidelity = random.uniform(0.0, 0.3)

        assert 0 <= fitness <= 1.0
        assert 0 <= fidelity <= 1.0

        self.fitness = fitness
        self.fidelity = fidelity
        self.lineage = lineage

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
        """
        Core of model - establishes relationship between parent and offspring
        """

        p_reproduce = parent.fitness if factors['P_REPRODUCE'] == 0 else factors['P_REPRODUCE']
        if not get_random_boolean(p_reproduce):
            return []

        fidelity_fidelity = parent.fidelity if factors['CORRELATED'] else random.random()
        offspring = []

        for i in range(random.randint(0, factors['N_OFFSPRING'])):
            fitness = derive(parent.fitness, parent.fidelity)
            fidelity = derive(parent.fidelity, fidelity_fidelity)
            offspring.append(Element(parent.lineage, fitness, fidelity))
        return offspring

    return [x for y in population for x in get_offspring(factors, y)]


def selection(factors, population):
    return [x for x in population if get_random_boolean(
        x.fitness if factors['P_SELECTION'] == 0 else factors['P_SELECTION']
    )]


def apply_environment_change(environment, population):

    lineages = {}
    new_population = []

    for e in population:
        if e.lineage in lineages.keys():
            delta_fitness = lineages[e.lineage]
        else:
            delta_fitness = random.gauss(environment[0], environment[1])
            lineages[e.lineage] = delta_fitness  # first seen (i.e. random choice) element sets change for lineage

        new_fitness = min(1.0, max(0.0, (e.fitness + delta_fitness)))  # bound to [0,1], don't worry about shape
        new_population.append(Element(e.lineage, new_fitness, e.fidelity))

    return new_population


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
    population_limit *= original_population_size  # stop when population size reaches a multiple of original population

    # starting summary
    initial_summary = get_population_summary(population, 0)
    results = [initial_summary]  # headers and starting conditions

    for t in range(1, generations+1):

        parent_population = selection(factors, population)
        offspring_population = reproduction(factors, population)
        population = parent_population + offspring_population

        if len(population) > original_population_size:  # if fixed population size
            population = random.sample(population, original_population_size)
        if len(population) < 3 or len(population) > population_limit:
            break

        results.append(get_population_summary(population, t))

        population = apply_environment_change(environment[t % len(environment)], population)

    lineages = [e.lineage for e in population]
    from collections import Counter
    print("g={0} {1}".format(t, Counter(lineages)))

    return results
