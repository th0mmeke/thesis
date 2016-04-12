import random
import model

GENERATIONS = 500
POPULATION_SIZE = 5000
N_ENVIRONMENTS = 10
N_REPEATS = 3
N_BUCKETS = 100
LOW_START = True

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
experiments = [
    # X1  X2  X3  X4  X5  X6  X7
    #--------------------------
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

# http://www.itl.nist.gov/div898/handbook/pri/section3/eqns/2to5m2.txt
experiments = [  # factors ordered by sorted order of factor_defns keys
    [0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1],
    [1, 1, 0, 1, 0],
    [0, 0, 1, 1, 0],
    [1, 0, 1, 0, 1],
    [0, 1, 1, 0, 0],
    [1, 1, 1, 1, 1],
]


def init_population(n, low_start):
    return [model.Element(low_start=low_start) for x in range(0, n)]


def generate_environments(n, generations):
    environments = []
    for i in range(0, n):
        # Environment is an array 1..period of list 1..N_BUCKETS of real
        environment = []
        for t in range(1, random.randint(5, generations)):
            environment.append([random.random() for bucket in range(0, N_BUCKETS)])
        environments.append(environment)
    return environments


factor_defns = {
    'P_REPRODUCE': [0, 0.66],
    'P_SELECTION': [0,	0.66],
    'N_OFFSPRING': [2, 5],
    'RESTRICTION': [False, True],
    'CORRELATED': [False, True],
}


def construct_line(run_number, experiment_number, result, factors):
    line = {
        'experiment': experiment_number,
        'run': run_number,
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

    f = open("results.data", "w")

    environments = generate_environments(N_ENVIRONMENTS, GENERATIONS)
    experiment_number = 0
    run_number = 0

    for experiment in experiments:

        factors = {k: factor_defns[k][v] for k, v in zip(factor_defns.keys(), experiment)}

        for environment in environments:

            for repeat in range(0, N_REPEATS):

                print("{0}/{1}".format(run_number + 1, N_REPEATS * len(environments) * len(experiments)))
                results = model.run(factors=factors,
                                    population=init_population(POPULATION_SIZE, LOW_START),
                                    generations=GENERATIONS,
                                    population_limit=10,
                                    environment=environment)

                if run_number == 0:
                    f.write(
                        format_results_header(construct_line(run_number, experiment_number, results[0], factors)) + "\n"
                    )

                f.write("\n".join([format_results_line(
                    construct_line(run_number, experiment_number, result, factors)
                ) for result in results]))
                f.write("\n")

                run_number += 1

        experiment_number += 1

    f.close()

if __name__ == "__main__":
    main()
