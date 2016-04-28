import random
import model

GENERATIONS = 500
POPULATION_SIZE = 5000
N_REPEATS = 3
N_ENVIRONMENTS = 100
MAX_SD = 0.5


experiments = [  # factors ordered by sorted order of factor_defns keys
    # ['BY_LINEAGE', 'CORRELATED', 'N_OFFSPRING', 'P_REPRODUCE', 'P_SELECTION', 'RESTRICTION']
    [1, 1, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 1]
]


def init_population(n):
    return [model.Element(x) for x in range(0, n)]  # assign sequential lineage IDs


def generate_environments():
    # Environment change is modelled as a change in the relationship between entity and environment.

    # Entity is represented by a fitness and a fidelity (to parent)
    # The difficulty is in how to connect fidelity and fitness (both composites) to environmental change.
    # Without knowing the specifics of the change, and modelling the reaction of each entity to that change,
    # we can only model abstracts.

    # Parental relationships provide a lineage, where related entities should have a similar response to change
    # In other words, environmental change is a change in fitness, but one where the change is conditioned
    # by lineage.

    return [(0, random.uniform(0, MAX_SD)) for i in range(0, N_ENVIRONMENTS)]  # (theta, sd)
    #return [(random.uniform(-MAX_SD, MAX_SD), random.uniform(0, MAX_SD)) for i in range(0, N_ENVIRONMENTS)]  # (theta, sd)

factor_defns = {
    'P_REPRODUCE': [0, 0.66],
    'P_SELECTION': [0, 0.66],
    'N_OFFSPRING': [2, 5],
    'RESTRICTION': [False, True],
    'CORRELATED': [False, True],
    'BY_LINEAGE': [False, True]
}


def construct_line(run_number, experiment_number, environment, result, factors):
    line = {
        'experiment': experiment_number,
        'run': run_number,
        'ar_theta': environment[0],
        'ar_sd': environment[1]
    }
    line.update(result)
    line.update({k: factor_defns[k].index(v) for k, v in factors.items()})  # convert back from values to factor levels
    return line


def format_results_line(line):
    return ",".join([str(line[x]) for x in sorted(line.keys())])


def format_results_header(line):
    return ",".join([str(x) for x in sorted(line.keys())])


def main():

    assert len(factor_defns) == len(experiments[0])  # Same order - must use appropriate design

    f = open("results.csv", "w")

    environments = generate_environments()
    experiment_number = 0
    run_number = 0

    for experiment in experiments:

        factors = {k: factor_defns[k][v] for k, v in zip(sorted(factor_defns.keys()), experiment)}

        for environment in environments:

            for repeat in range(0, N_REPEATS):

                print("{0}/{1}".format(run_number + 1, N_REPEATS * len(environments) * len(experiments)))
                results = model.run(factors=factors,
                                    population=init_population(POPULATION_SIZE),
                                    generations=GENERATIONS,
                                    population_limit=10,
                                    environment=environment)

                if run_number == 0:
                    f.write(format_results_header(construct_line(run_number,
                                                                 experiment_number,
                                                                 environment,
                                                                 results[0],
                                                                 factors)) + "\n")

                f.write("\n".join([format_results_line(
                    construct_line(run_number, experiment_number, environment, result, factors)
                ) for result in results]))
                f.write("\n")

                run_number += 1

        experiment_number += 1

    f.close()

if __name__ == "__main__":
    main()


# # http://www.itl.nist.gov/div898/handbook/pri/section3/eqns/2to6m3.txt
# experiments = [
#    [0,  0,  0,  1,  1,  1],
#    [1,  0,  0,  0,  0,  1],
#    [0,  1,  0,  0,  1,  0],
#    [1,  1,  0,  1,  0,  0],
#    [0,  0,  1,  1,  0,  0],
#    [1,  0,  1,  0,  1,  0],
#    [0,  1,  1,  0,  0,  1],
#    [1,  1,  1,  1,  1,  1]
# ]

# http://www.itl.nist.gov/div898/handbook/pri/section3/eqns/2to7m3.txt
# experiments = [
#     # X1  X2  X3  X4  X5  X6  X7
#     #--------------------------
#     [0,  0,  0,  0,  0,  0,  0],
#     [1,  0,  0,  0,  1,  0,  1],
#     [0,  1,  0,  0,  1,  1,  0],
#     [1,  1,  0,  0,  0,  1,  1],
#     [0,  0,  1,  0,  1,  1,  1],
#     [1,  0,  1,  0,  0,  1,  0],
#     [0,  1,  1,  0,  0,  0,  1],
#     [1,  1,  1,  0,  1,  0,  0],
#     [0,  0,  0,  1,  0,  1,  1],
#     [1,  0,  0,  1,  1,  1,  0],
#     [0,  1,  0,  1,  1,  0,  1],
#     [1,  1,  0,  1,  0,  0,  0],
#     [0,  0,  1,  1,  1,  0,  0],
#     [1,  0,  1,  1,  0,  0,  1],
#     [0,  1,  1,  1,  0,  1,  0],
#     [1,  1,  1,  1,  1,  1,  1]
# ]

# http://www.itl.nist.gov/div898/handbook/pri/section3/eqns/2to5m2.txt
# experiments = [  # factors ordered by sorted order of factor_defns keys
#     [0, 0, 0, 1, 1],
#     [1, 0, 0, 0, 0],
#     [0, 1, 0, 0, 1],
#     [1, 1, 0, 1, 0],
#     [0, 0, 1, 1, 0],
#     [1, 0, 1, 0, 1],
#     [0, 1, 1, 0, 0],
#     [1, 1, 1, 1, 1],
# ]