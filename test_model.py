import unittest
import statistics
import model

class TestModel(unittest.TestCase):

    def test_get_random_boolean(self):
        positive = 0
        for i in range(0,100):
            if model.get_random_boolean(1.0,1.0):
                positive +=1
        self.assertEqual(100,positive)

        positive = 0
        for i in range(0,100):
            if model.get_random_boolean(0.0,1.0):
                positive +=1
        self.assertEqual(0,positive)

        positive = 0
        for i in range(0,10000):
            if model.get_random_boolean(0.5,0.5):
                positive +=1
        self.assertIn(positive, range(2350,2650)) # should be 250-ish

    # def test_gaussian_derive(self):
    #     for i in range(0,1000):
    #         x = model.gaussian_derive(0.5, 7.0) # should result in clipping
    #         self.assertTrue(0.0<=x<=1.0)
    #     samples = []
    #     for i in range(0,1000):
    #         samples.append(model.gaussian_derive(0.5,0.8))
    #     self.assertTrue(0.18<statistics.stdev(samples)<0.22)
    #     self.assertTrue(0.49<statistics.mean(samples)<0.51)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
