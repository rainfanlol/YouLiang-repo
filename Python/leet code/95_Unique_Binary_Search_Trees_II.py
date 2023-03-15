"""
Given an integer n, return all the structurally unique BST's (binary search trees), which has exactly n nodes of unique values from 1 to n. Return the answer in any order.
"""


from typing import List
import unittest

class Solution:
    class TreeNode:
        def __init__(self, val=0, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    def generateTrees(self, n: int) -> List[TreeNode]:
        if n == 0:
            return []
        return self.helper(1, n)
    
    def helper(self, start: int, end: int) -> List[TreeNode]:
        if start > end:
            return [None]
        result = []
        for i in range(start, end+1):
            left_subtrees = self.helper(start, i-1)
            right_subtrees = self.helper(i+1, end)
            for left in left_subtrees:
                for right in right_subtrees:
                    root = self.TreeNode(i)
                    root.left = left
                    root.right = right
                    result.append(root)
        return result if result else [None]

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.s = Solution()
    
    def test_generateTrees(self):
        n1 = 3
        expected_output1 = [
            Solution.TreeNode(1, None, Solution.TreeNode(2, None, Solution.TreeNode(3))),
            Solution.TreeNode(1, None, Solution.TreeNode(3, Solution.TreeNode(2))),
            Solution.TreeNode(2, Solution.TreeNode(1), Solution.TreeNode(3)),
            Solution.TreeNode(3, Solution.TreeNode(1, None, Solution.TreeNode(2)), None),
            Solution.TreeNode(3, Solution.TreeNode(2, Solution.TreeNode(1)), None),
        ]
        output1 = self.s.generateTrees(n1)
        self.assertEqual(len(expected_output1), len(output1))
        self.assertSetEqual(set(map(str, expected_output1)), set(map(str, output1)))
        
        n2 = 1
        expected_output2 = [Solution.TreeNode(1)]
        output2 = self.s.generateTrees(n2)
        self.assertEqual(expected_output2, output2)
        
if __name__ == '__main__':
    unittest.main()


