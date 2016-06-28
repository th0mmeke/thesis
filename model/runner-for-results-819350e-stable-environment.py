import os
import random
import itertools
import model

#experiments = [[1,  1,  1,  1,  1,  1]]

def dist_a(source, correlation):
    return max(0.0,min(1.0, random.gauss(source, 1.0-correlation)))

def dist_b(source, correlation):
    x = random.gauss(source, 1.0-correlation)
    while x < 0.0 or x > 1.0:
        x = random.gauss(source, 1.0-correlation)
    assert x >= 0.0 and x <= 1.0
    return x

def dist_c(source, correlation):
    return random.uniform(0, 1)

def change_a(factors, population, gen, ecf):
    if ecf > 0 & gen % ecf == 0:
        return [Element(factors[4](x.fitness-0.2, 0.70), x.correlation) for x in population]
    else:
        return population


def change_b(factors, population, gen, ecf):
    if ecf > 0:
        return [Element(factors[4](x.fitness-(0.2/ecf), 0.70), x.correlation) for x in population]
    else:
        return population

factor_defns = [
    [0, 0.66],          # 0 = P_REPRODUCE
    [0,	0.66],          # 1 = P_SELECTION
    [2, 5],             # 2 = N_OFFSPRING
    [False],                # 3 = RESTRICTION
    [dist_a, dist_b],   # 4 - shape of distribution
    [True],      # 5 = CORRELATION_CORRELATION
]

experiments = list(itertools.product(range(len(factor_defns[0])),
                                range(len(factor_defns[1])),
                                range(len(factor_defns[2])),
                                range(len(factor_defns[3])),
                                range(len(factor_defns[4])),
                                range(len(factor_defns[5]))));

def init_population(n, low_start):
    return [model.Element(low_start = low_start) for x in range(0,n)]

def main():

    low_start = True
    f = open("results.data", "w")

    # Write initial header line to file
    str_factors = "p_reproduce,p_selection,n_offspring,truncate,distribution,correlation_correlation,shape,ecf"
    _summary = model.get_population_summary(init_population(2,low_start),0)
    str_header = ",".join([x for x in _summary.keys()])
    f.write('exp,run,' + str_header + "," + str_factors + "\n")

    expCount = 0
    for experiment in experiments:

        factors = [factor_defn[factor_value] for factor_value, factor_defn in zip(experiment, factor_defns)]

        for environment_change_frequency in [0]:
            experiment_factors = ",".join([str(x) for x in experiment]) + "," + str(environment_change_frequency)
            for repeat in range(0, 10):
                print("{0}/{1} {3} {2} {4}".format(expCount+1, len(experiments), environment_change_frequency, repeat, factors))
                results = model.run(factors, population=init_population(5000, low_start), generations=500, population_limit=10, environment_change_frequency=environment_change_frequency)
                array_results = []
                for generation in results:
                    str_generation = ",".join([str(x) for x in generation.values()])
                    array_results.append( ",".join([str(expCount),str(expCount*10+repeat), str_generation, experiment_factors]))
                f.write("\n".join(array_results))
                f.write("\n")

            print("\n")
            expCount+=1

    f.close()

if __name__ == "__main__":
    main()
