import os
import random
import itertools
import model

# http://www.itl.nist.gov/div898/handbook/pri/section3/eqns/2to6m3.txt
# experiments = [
# #   X1  X2  X3  X4  X5  X6
# #   ----------------------
# [0,  0,  0,  1,  1,  1],
# [0,  0,  0,  1,  1,  1],
# [1,  0,  0,  0,  0,  1],
# [0,  1,  0,  0,  1,  0],
# [1,  1,  0,  1,  0,  0],
# [0,  0,  1,  1,  0,  0],
# [1,  0,  1,  0,  1,  0],
# [0,  1,  1,  0,  0,  1],
# [1,  1,  1,  1,  1,  1]
# ]

# http://www.itl.nist.gov/div898/handbook/pri/section3/eqns/2to7m3.txt
experiments = [
#   X1  X2  X3  X4  X5  X6  X7
#   --------------------------
    [0,  0,  1,  0,  1,  1,  1],
    [1,  0,  1,  0,  0,  1,  0],
    [0,  1,  1,  0,  0,  0,  1],
    [1,  1,  1,  0,  1,  0,  0],
    [0,  0,  1,  1,  1,  0,  0],
    [1,  0,  1,  1,  0,  0,  1],
    [0,  1,  1,  1,  0,  1,  0],
    [1,  1,  1,  1,  1,  1,  1]
]

# experiments = itertools.product(range(2), repeat=7)
# experiments = [[0,0,0,0,0,1,1], [0,0,0,1,0,1,1]]
# experiments = [[0,0,0,1,1,1,1]]

factor_defns = [
    [0.33,     0.66],    # 0 = P_REPRODUCE - 0 = fitness
    [0.33,     0.66],    # 1 = P_SELECTION - 0 = fitness
    [2,        5],      # 2 = N_OFFSPRING
    [False,    True],   # 3 = RESTRICTION - False = sample, True = truncate
    # gauss is described by mean=source, sd=1-correlation, then clipped to [0,1]
    # uniform to range [source-(1-correlation), source+(1+correlation)], then clipped to [0,1]
    [lambda source, correlation: max(0.0,min(1.0, random.gauss(source, 1.0-correlation))), lambda source, correlation: max(0.0,min(1.0, random.uniform(source-(1.0-correlation), source+(1.0-correlation))))],
    [False,    True],   # 5 = FITNESS_CORRELATION
    [False,    True],   # 6 = CORRELATION_CORRELATION
]

def init_population(n, low_start):
    return [model.Element(low_start = low_start) for x in range(0,n)]

def main():

    low_start = False
    f = open("results.data", "w")

    # Write initial header line to file
    str_factors = "p_reproduce,p_selection,n_offspring,truncate,distribution,fitness_correlation,correlation_correlation,environment_change_frequency"
    _summary = model.get_population_summary(init_population(2,low_start),0)
    str_header = ",".join([x for x in _summary.keys()])
    f.write(str_header + "," + str_factors + "\n")

    for experiment in experiments:

        factors = [factor_defn[factor_value] for factor_value, factor_defn in zip(experiment, factor_defns)]

        for environment_change_frequency in [0,1,5,10]:
            experiment_factors = ",".join(["1" if x==1 else "-1" for x in experiment]) + "," + str(environment_change_frequency)
            for repeat in range(0,10):
                print(repeat, factors)
                results = model.run(factors, population=init_population(5000, low_start), generations=500, population_limit=10, environment_change_frequency=environment_change_frequency)
                f.write("\n".join([",".join([str(x) for x in generation.values()]) + "," + experiment_factors for generation in results]))
                f.write("\n")

            print("\n")

    f.close()

if __name__ == "__main__":
    main()
