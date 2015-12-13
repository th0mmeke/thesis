import os
import random
import model

experiments = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [1,  0,  0,  0,  0,  1,  1,  1],
    [0,  1,  0,  0,  1,  0,  1,  1],
    [1,  1,  0,  0,  1,  1,  0,  0],
    [0,  0,  1,  0,  1,  1,  1,  0],
    [1,  0,  1,  0,  1,  0,  0,  1],
    [0,  1,  1,  0,  0,  1,  0,  1],
    [1,  1,  1,  0,  0,  0,  1,  0],
    [0,  0,  0,  1,  1,  1,  0,  1],
    [1,  0,  0,  1,  1,  0,  1,  0],
    [0,  1,  0,  1,  0,  1,  1,  0],
    [1,  1,  0,  1,  0,  0,  0,  1],
    [0,  0,  1,  1,  0,  0,  1,  1],
    [1,  0,  1,  1,  0,  1,  0,  0],
    [0,  1,  1,  1,  1,  0,  0,  0],
    [1,  1,  1,  1,  1,  1,  1,  1]
]

factor_defns = [
    [0.0,      1.0],    # 0 = P_REPRODUCE - 0 = fitness
    [0.0,      1.0],    # 1 = P_SELECTION - 0 = fitness
    [2,        5],      # 2 = N_OFFSPRING
    [False,    True],   # 3 = TRUNCATE_POPULATION RANDOMLY
    [lambda source, correlation: max(0.0,min(1.0, random.gauss(source, 1.0-correlation))), lambda source, correlation: max(0.0,min(1.0, random.uniform(source, 1.0-correlation)))],
    [False,    True],   # 5 = FITNESS_CORRELATION
    [False,    True],   # 6 = CORRELATION_CORRELATION
    [False,    True]    # 7 = Start with low values for correlation and fitness
]

def init_population(factors, n):
    return [model.Element(factors) for x in range(0,n)]

f = open("results.data", "w")

header_added = False
header = "p_reproduce, p_selection, n_offspring, truncate, distribution, fitness_correlation, correlation_correlation, low_start"

for experiment in experiments:

    factors = [factor_defn[factor_value] for factor_value, factor_defn in zip(experiment, factor_defns)]
    print(factors)
    experiment_factors = ",".join([str(x) for x in experiment])

    for repeat in range(0,1):
        results = model.run(factors, population=init_population(factors, 1000), generations=50, population_limit=10)

        if not header_added:
            f.write(",".join(results.keys()) + header + "\n")
            header_added = True

        str_results = [str(x) for x in results.values()]
        f.write(",".join(str_results) + "," + experiment_factors + "\n")

    print("\n")

f.close()
