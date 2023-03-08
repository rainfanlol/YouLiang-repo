"""
Given two integers n and k, return all possible combinations of k numbers chosen from the range [1, n].

You may return the answer in any order.
"""

import unittest

class Solution:
    def combine(self, n: int, k: int) :
        res = []
        self.dfs(list(range(1,n+1)), k, 0, [], res)
        return res
    
    def dfs(self, nums, k, index, path, res):
        if k == 0:
            res.append(path)
            return
        for i in range(index, len(nums)):
            self.dfs(nums, k-1, i+1, path+[nums[i]], res)


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.s = Solution()

    def test_combine_1(self):
        n = 4
        k = 2
        expected = [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
        self.assertEqual(self.s.combine(n, k), expected)

    def test_combine_2(self):
        n = 1
        k = 1
        expected = [[1]]
        self.assertEqual(self.s.combine(n, k), expected)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
