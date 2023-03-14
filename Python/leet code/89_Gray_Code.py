"""
An n-bit gray code sequence is a sequence of 2n integers where:

Every integer is in the inclusive range [0, 2n - 1],

The first integer is 0,

An integer appears no more than once in the sequence,

The binary representation of every pair of adjacent integers differs by exactly one bit, and

The binary representation of the first and last integers differs by exactly one bit.

Given an integer n, return any valid n-bit gray code sequence.
"""
import unittest
from typing import List

class Solution:
    def grayCode(self, n: int) -> List[int]:
        res = [0]
        for i in range(n):
            res += [x + pow(2, i) for x in reversed(res)]
        return res

class TestSolution(unittest.TestCase):
    def test_example1(self):
        s = Solution()
        n = 2
        expected_output = [0,1,3,2]
        self.assertEqual(s.grayCode(n), expected_output)

    def test_example2(self):
        s = Solution()
        n = 1
        expected_output = [0,1]
        self.assertEqual(s.grayCode(n), expected_output)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
