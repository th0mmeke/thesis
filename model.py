import random
import math
import statistics

# VERY SENSITIVE TO ABSOLUTE FITNESS - goes extinct with max initial fitness below 0.29 or so if no way to improve fitness beyond that

# Endogenise fitness (make relative) and population (restriction from resource constraints)
# Show: from low correlation to high correlation (inheritance)
# Show: from highest correlation to high correlation (inheritance)

# Controls: fitness and correlation
# Independent - offspring fitness correlated with parent, but not correlation
# Dependent - offspring fitness and correlation based on parent's

# TODO:
# relate to bourrat results
# run with independent fitness/correlation
# Sensitivity - experiment design to determine effect of each parameter - ANOVA
# Sensitivity - experiment runner


# BUILDING BLOCKS
def gaussian_derive(source, correlation):
    '''
    Source and correlation as mean and s.d., respectively, of a gaussian (normal) distribution
    '''
    return max(0.0,min(1.0, random.gauss(source, correlation)))

# SKELETON
class Element:
    def __init__(self, fitness=None, correlation=None):
        self.fitness = fitness if fitness != None else random.uniform(0.0,0.3)
        self.correlation = correlation if correlation != None else random.uniform(0.0,0.5)

    def __str__(self):
        return str(self.fitness)

def get_random_boolean(p1, p2):
    return random.random() < (p1*p2)  # assumes uniform distribution?

def reproduction(population):
    return [x for y in population for x in get_offspring(y)]

def selection(population):
    return [x for x in population if get_random_boolean(x.fitness,P_SURVIVE)]

def truncate_population(population):
    return population

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

def run(population,generations):

    for i in range(0,generations):

        print(get_population_summary(population, i))

        parent_population = selection(population)
        offspring_population = reproduction(population)
        population = parent_population + offspring_population
        population = truncate_population(population)

        if len(population) == 0:
            break

    return population

#print([str(x) for x in population])
