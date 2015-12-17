import os
import random
import itertools
import model

# http://www.itl.nist.gov/div898/handbook/pri/section3/eqns/2to7m3.txt
experiments = [
#   X1  X2  X3  X4  X5  X6  X7
#   --------------------------
    [0,  0,  0,  0,  0,  0,  0],
    [1,  0,  0,  0,  1,  0,  1],
    [0,  1,  0,  0,  1,  1,  0],
    [1,  1,  0,  0,  0,  1,  1],
    [0,  0,  1,  0,  1,  1,  1],
    [1,  0,  1,  0,  0,  1,  0],
    [0,  1,  1,  0,  0,  0,  1],
    [1,  1,  1,  0,  1,  0,  0],
    [0,  0,  0,  1,  0,  1,  1],
    [1,  0,  0,  1,  1,  1,  0],
    [0,  1,  0,  1,  1,  0,  1],
    [1,  1,  0,  1,  0,  0,  0],
    [0,  0,  1,  1,  1,  0,  0],
    [1,  0,  1,  1,  0,  0,  1],
    [0,  1,  1,  1,  0,  1,  0],
    [1,  1,  1,  1,  1,  1,  1]
]
#experiments = itertools.product(range(2), repeat=8)

factor_defns = [
    [0.0,      1.0],    # 0 = P_REPRODUCE - 0 = fitness
    [0.0,      1.0],    # 1 = P_SELECTION - 0 = fitness
    [2,        5],      # 2 = N_OFFSPRING
    [False,    True],   # 3 = TRUNCATE_POPULATION RANDOMLY
    # gauss is described by mean=source, sd=1-correlation, then clipped to [0,1]
    # uniform to range [source-(1-correlation), source+(1+correlation)], then clipped to [0,1]
    [lambda source, correlation: max(0.0,min(1.0, random.gauss(source, 1.0-correlation))), lambda source, correlation: max(0.0,min(1.0, random.uniform(source-(1.0-correlation), source+(1.0-correlation))))],
    [False,    True],   # 5 = FITNESS_CORRELATION
    [False,    True],   # 6 = CORRELATION_CORRELATION
]

def init_population(n, low_start):
    return [model.Element(low_start = low_start) for x in range(0,n)]

def main():

    changing_environment = True
    low_start = True

    f = open("results.data", "w")

    header_added = False
    header = "p_reproduce, p_selection, n_offspring, truncate, distribution, fitness_correlation, correlation_correlation"

    for experiment in experiments:

        factors = [factor_defn[factor_value] for factor_value, factor_defn in zip(experiment, factor_defns)]
        print(factors)
        experiment_factors = ",".join(["1" if x==1 else "-1" for x in experiment])

        for repeat in range(0,10):
            (initial, final) = model.run(factors, population=init_population(5000, low_start), generations=250, population_limit=10, changing_environment=changing_environment)

            if not header_added: # use the header information returned from the model, but only once
                initial_header = ",".join(["initial_" + x for x in initial.keys()])
                final_header = ",".join(["final_" + x for x in final.keys()])
                f.write(initial_header + "," + final_header + "," + header + "\n")
                header_added = True

            str_initial = ",".join([str(x) for x in initial.values()])
            str_final = ",".join([str(x) for x in final.values()])
            f.write(str_initial + "," + str_final + "," + experiment_factors + "\n")

        print("\n")

    f.close()

if __name__ == "__main__":
    main()
