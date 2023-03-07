"""
You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?
"""

import unittest

class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        if n == 2:
            return 2
        dp = [0] * (n+1)
        dp[1] = 1
        dp[2] = 2
        for i in range(3, n+1):
            dp[i] = dp[i-1] + dp[i-2]
        return dp[n]


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.s = Solution()

    def test_example1(self):
        self.assertEqual(self.s.climbStairs(2), 2)

    def test_example2(self):
        self.assertEqual(self.s.climbStairs(3), 3)

    def test_custom1(self):
        self.assertEqual(self.s.climbStairs(1), 1)

    def test_custom2(self):
        self.assertEqual(self.s.climbStairs(5), 8)

    def test_custom3(self):
        self.assertEqual(self.s.climbStairs(6), 13)

if __name__ == '__main__':
    unittest.main()