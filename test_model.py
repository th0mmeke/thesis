import unittest
import model

class TestModel(unittest.TestCase):

    def test_get_random_boolean(self):
        positive = 0
        for i in range(0,100):
            if get_random_boolean(1.0,1.0):
                positive +=1

        self.assertEquals(100,positive)
