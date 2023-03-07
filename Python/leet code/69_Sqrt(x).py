"""
Given a non-negative integer x, return the square root of x rounded down to the nearest integer. The returned integer should be non-negative as well.

You must not use any built-in exponent function or operator.

For example, do not use pow(x, 0.5) in c++ or x ** 0.5 in python.
"""
import unittest

class Solution:
    def mySqrt(self,x: int) -> int:
        if x == 0:
            return 0
        
        left, right = 1, x
        while left <= right:
            mid = (left + right) // 2
            if mid * mid == x:
                return mid
            elif mid * mid < x:
                left = mid + 1
            else:
                right = mid - 1
                
        return right

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.s = Solution()

    def test_example1(self):
        self.assertEqual(self.s.mySqrt(4), 2)

    def test_example2(self):
        self.assertEqual(self.s.mySqrt(8), 2)

    def test_custom1(self):
        self.assertEqual(self.s.mySqrt(1), 1)

    def test_custom2(self):
        self.assertEqual(self.s.mySqrt(0), 0)

    def test_custom3(self):
        self.assertEqual(self.s.mySqrt(2), 1)

    def test_custom4(self):
        self.assertEqual(self.s.mySqrt(2147395599), 46339)


if __name__ == '__main__':
    unittest.main()
