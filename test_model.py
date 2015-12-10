import unittest
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
        self.assertIn(positive, range(2400,2599)) # should be 250-ish


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
