"""
Given an integer n, return the number of structurally unique BST's (binary search trees) which has exactly n nodes of unique values from 1 to n.
"""

import unittest

class Solution:
    def numTrees(self, n: int) -> int:
        dp = [0] * (n + 1)
        dp[0] = 1
        for i in range(1, n + 1):
            for j in range(1, i + 1):
                dp[i] += dp[j - 1] * dp[i - j]
        return dp[n]


class TestSolution(unittest.TestCase):
    def test_numTrees(self):
        s = Solution()
        self.assertEqual(s.numTrees(3), 5)
        self.assertEqual(s.numTrees(1), 1)

if __name__ == '__main__':
    unittest.main()