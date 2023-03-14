"""
Given an integer array nums that may contain duplicates, return all possible 

subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.
"""
import unittest
from typing import List

class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        def backtrack(start, path):
            res.append(path[:])
            for i in range(start, len(nums)):
                if i > start and nums[i] == nums[i-1]:
                    continue
                path.append(nums[i])
                backtrack(i+1, path)
                path.pop()

        res = []
        nums.sort()
        backtrack(0, [])
        return res


class TestSolution(unittest.TestCase):
    def test_example1(self):
        s = Solution()
        nums = [1,2,2]
        expected_output = [[],[1],[1,2],[1,2,2],[2],[2,2]]
        self.assertEqual(s.subsetsWithDup(nums), expected_output)

    def test_example2(self):
        s = Solution()
        nums = [0]
        expected_output = [[],[0]]
        self.assertEqual(s.subsetsWithDup(nums), expected_output)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
