import unittest
import statistics
import model
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

    def test_lambda_distributions(self):
        gauss = factor_defns[4][0]
        uniform = factor_defns[4][1]
        # both restricted to range [0,1]
        # gauss is described by mean=source, sd=1-correlation, then clipped to [0,1]
        # uniform to range [source-(1-correlation), source+(1+correlation)], then clipped to [0,1]
        gauss_values = []
        for i in range(0,1000):
            gauss_values.append(gauss(0.5,0.7)) # mean in middle of range, so clipping won't introduce bias
        uniform_values = []
        for i in range(0,1000):
            uniform_values.append(uniform(0.5,0.7)) # mean in middle of range, so clipping won't introduce bias

        self.assertAlmostEqual(statistics.mean(gauss_values), statistics.mean(uniform_values), places=1)
        self.assertNotAlmostEqual(statistics.stdev(gauss_values), statistics.stdev(uniform_values), places=1)

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

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
