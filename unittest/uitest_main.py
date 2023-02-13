import unittest
from unittest_def import add, sub, multiply, divide

class TestDemo(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 3), 4)

    def test_sub(self):
        self.assertEqual(sub(5, 3), 2)

    def test_multiply(self):
        self.assertEqual(multiply(5, 3), 15)

    def test_divide(self):
        self.assertEqual(divide(6, 2), 3)

if __name__ == "__main__":
    unittest.main()