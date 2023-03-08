"""
Given an integer array nums of unique elements, return all possible 
subsets
 (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.
"""

import unittest
from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        # 初始化一個空集合，用於儲存結果
        res = [[]]
        for num in nums:
            # 將當前元素加入res中的每個子集
            for i in range(len(res)):
                res.append(res[i] + [num])
        return res

    
class TestSolution(unittest.TestCase):
    def test_example1(self):
        s = Solution()
        nums = [1, 2, 3]
        expected_output = [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
        self.assertEqual(s.subsets(nums), expected_output)

    def test_example2(self):
        s = Solution()
        nums = [0]
        expected_output = [[], [0]]
        self.assertEqual(s.subsets(nums), expected_output)

if __name__ == '__main__':
    unittest.main()
