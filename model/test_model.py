import unittest
import statistics
import model
import random
from runner import factor_defns
from runner import init_population

class TestModel(unittest.TestCase):

    def test_get_random_boolean(self):
        positive = 0
        for i in range(0,100):
            if model.get_random_boolean(1.0):
                positive +=1
        self.assertEqual(100,positive)

        positive = 0
        for i in range(0,100):
            if model.get_random_boolean(0.0):
                positive +=1
        self.assertEqual(0,positive)

    def test_regression_large_values(self):

        def dist_b(source, correlation):
            x = random.gauss(source, 1.0-correlation)
            while x < 0.0 or x > 1.0:
                x = random.gauss(source, 1.0-correlation)
            assert x >= 0.0 and x<=1.0
            return x

        factors = [0,1.0,2,True,dist_b,True,True,1]
        #factor_values = [0, 1, 0, 1, 1, 0, 1] # factor_defns[for selection] = 1.0, meaning no selection! So zero fitness entities persist...
        #factors = [defn[value] for defn, value in zip(factor_defns, factor_values)]
        #print(factors)
        results = model.run(factors, population=init_population(5000, low_start=True), generations=250, population_limit=10, environment_change_frequency=1)
        self.assertTrue(results[-1]['ave_cor'] >= 0 and results[-1]['ave_cor'] <= 1.0)

    def test_regression_zero_fitness(self):
        factors = [0,0,2,True,lambda source, correlation:max(0.0,min(1.0, random.gauss(source, 1.0-correlation))),False, True]
        results = model.run(factors, population=init_population(5000, True), generations=500, population_limit=10, environment_change_frequency=1)

    def test_selection(self):
        #return [x for x in population if get_random_boolean(x.fitness if factors[1] == 0 else factors[1])]
        population = [model.Element(0.0,0.0) for i in range(0,1000)]
        self.assertEqual(0,len(model.selection([0,0], population))) # use element fitness
        self.assertEqual(len(population), len(model.selection([0,1.0], population))) # use provided fitness = 1.0 so should be no selection

    def test_reproduction(self):

        def run_reproduction_test(factors):
            population = [model.Element(0.5) for x in range(0,1000)] # fitness=0 for all Elements
            return [len(model.reproduction(factors, population)) for i in range(0,100)]

        # Check case where no elements should be able to reproduce
        population = [model.Element(0) for x in range(0,1000)] # fitness=0 for all Elements
        self.assertEqual(0,len(model.reproduction([0], population))) # factors[0]=0 meaning use parent fitness (also 0)

        # Check number of offspring
        factors = [0,0,2,0,factor_defns[4][0],0,0] # [0]=0 - use parent fitness, [2] = 2 - n_offspring, mean=1, [4,5,6] - don't care but present
        values = run_reproduction_test(factors)
        self.assertAlmostEqual(500,statistics.mean(values),places=-2)

        factors = [0,0,4,0,factor_defns[4][0],0,0]
        values = run_reproduction_test(factors)
        self.assertAlmostEqual(1000,statistics.mean(values),places=-2)

    def test_tweak_fitness(self):

        factors = [0,0,0,0,factor_defns[4][0]]

        population = init_population(50, low_start=True)
        initial_fitness = [x.fitness for x in population]
        final_population = model.tweak_fitness(factors, population)
        final_fitness = [x.fitness for x in final_population]
        self.assertTrue(all([x.fitness >= 0.0 and x.fitness <= 1.0 for x in final_population]))
        # should use ANOVA to test hypothesis that means are the same, but needs scipy in python...so just test the means :)
        self.assertTrue(statistics.mean(initial_fitness) >= statistics.mean(final_fitness))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
