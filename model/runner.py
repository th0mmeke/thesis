import random
import model

GENERATIONS = 500
POPULATION_SIZE = 5000
N_REPEATS = 1
N_ENVIRONMENTS = 150
MAX_SD = 0.5

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

experiments = [  # factors ordered by sorted order of factor_defns keys
    [1, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 1, 1]
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

    # Modelling the change:

    # Environmental change can be represented by magnitude and periodicity -
    # or sample magnitudes from beta distribution described by two random numbers - easier than describing change
    # in other ways...

    # Modelling the EFFECT of change:

    # a) is to model without lineage, where just modify fitness without consideration of entity relationships,
    # and hence fidelity.
    # b) model lineage but without considering effect of fidelity.
    # All entities in a lineage have a related direction of change.
    # This makes most sense when fidelity overall is low, as under those conditions there is likely to be
    # significant overlap between lineages
    # c) model lineage incorporating fidelity.
    # The degree and direction of impact depends on the relationship between elements in a lineage. If a parent
    # experiences some impact, then the range of impact experienced by the child is proportional to the fidelity -
    # high fidelity means close correlation, low fidelity means a weak correlation.

    # Each environment is modelled as a possible range for individual changes to fitness at each generation
    # The range is given as a pair of upper and lower bounds for the fitness delta
    # The degree of correlation between generations is given by a third value, to model the roughness
    # or smoothness of change over time
    # A further refinement might be to introduce a probability of abrupt change, where the three values - uppper,
    # lower, and correlation - are all reset every so often. This though is not implemented at present.

    # The model can apply the change either to all entities, or each entity, or to a lineage
    # as these are the only ways we can distinguish and hence group entities.

    # def derive(source, correlation):
    #     x = random.gauss(source, correlation)
    #     while x < -MAX_DELTA or x > MAX_DELTA:
    #         x = random.gauss(source, correlation)
    #     return x
    #
    # environments = []
    # for i in range(0, n):
    #     e = []
    #     roughness = random.uniform(0, MAX_DELTA)  # no real reason for MAX_DELTA, just simpler
    #     bounds = sorted((random.uniform(-MAX_DELTA, MAX_DELTA), random.uniform(-MAX_DELTA, MAX_DELTA)))
    #     for j in range(0, GENERATIONS):
    #         assert (-MAX_DELTA <= bounds[0] <= MAX_DELTA)
    #         assert (-MAX_DELTA <= bounds[1] <= MAX_DELTA)
    #         assert (bounds[0] <= bounds[1])
    #         e.append(bounds)
    #         bounds = sorted((derive(bounds[0], roughness), derive(bounds[1], roughness)))
    #     environments.append(e)

    return [(random.uniform(-MAX_SD, MAX_SD), random.uniform(0, MAX_SD)) for i in range(0, N_ENVIRONMENTS)]  # (theta, sd)


def read_environments():
    import csv
    environments = []
    with open('../results/environments.csv') as environments_file:
        reader = csv.reader(environments_file)
        for row in reader:
            e = []
            for mean in row:
                e.append([float(mean) - MAX_SD, float(mean) + MAX_SD])
            environments.append(e)

    return environments

factor_defns = {
    'P_REPRODUCE': [0, 0.66],
    'P_SELECTION': [0,	0.66],
    'N_OFFSPRING': [2, 5],
    'RESTRICTION': [False, True],
    'CORRELATED': [False, True],
    'BYLINEAGE': [False, True]
}


def construct_line(run_number, experiment_number, environment, result, factors):
    line = {
        'experiment': experiment_number,
        'run': run_number,
        'ari_theta': environment[0],
        'ari_sd': environment[1]
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

        factors = {k: factor_defns[k][v] for k, v in zip(factor_defns.keys(), experiment)}

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
