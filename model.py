import random
import math
import statistics

# Endogenise fitness (make relative) and population (restriction from resource constraints)
# Show: from low correlation to high correlation (inheritance)
# Show: from highest correlation to high correlation (inheritance)

# Independent - offspring fitness correlated with parent, but not correlation
# Dependent - offspring fitness and correlation based on parent's

# SKELETON
class Element:
    def __init__(self, factors, fitness=None, correlation=None):
        self.fitness = fitness if fitness != None else random.uniform(0.0,0.3 if factors[7] else 0.9)
        self.correlation = correlation if correlation != None else random.uniform(0.0 if factors[7] else 0.5,0.3 if factors[7] else 0.9)

    def __str__(self):
        return str(self.fitness)

def get_random_boolean(p):
    return random.random() < p

def reproduction(factors, population):

    def get_offspring(factors, parent):
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
    ave_fitness = math.fsum([x.fitness for x in population])/len(population)
    ave_correlation = math.fsum([x.correlation for x in population])/len(population)

    if len(population) > 1:
        sd_fitness = statistics.stdev([x.fitness for x in population])
        sd_correlation = statistics.stdev([x.correlation for x in population])
        format_string = "{0:>5} {1:>10} {2:10.2f} {3:10.2f} {4:12.2f} {5:10.2f}"
    else:
        sd_fitness = sd_correlation = "n/a"
        format_string = "{0:>5} {1:>10} {2:10.2f} {3:>10} {4:12.2f} {5:>10}"

    summary = format_string.format(generation, len(population), ave_fitness, sd_fitness, ave_correlation, sd_correlation)
    if generation==0:
        header = "\n{0:>5} {1:>10} {2:>10} {3:>10} {4:>12} {5:>10}\n".format("gen","pop","ave fit","sd fit","ave cor","sd cor")
        return header + summary
    else:
        return summary

def run(factors, population, generations, population_limit):

    original_population_size = len(population)
    population_limit *= original_population_size # multiple of original population

    for i in range(0,generations):

        print(get_population_summary(population, i))

        parent_population = selection(factors, population)
        offspring_population = reproduction(factors, population)
        population = parent_population + offspring_population
        if factors[3] and len(population) > original_population_size:
            population = random.sample(population, original_population_size)

        if len(population) == 0 or len(population) > population_limit:
            break

    return population

#print([str(x) for x in population])
