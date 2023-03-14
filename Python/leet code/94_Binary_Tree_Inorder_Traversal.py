"""
Given the root of a binary tree, return the inorder traversal of its nodes' values.
"""

import unittest
from typing import List

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def inorderTraversal(self, root: TreeNode) -> List[int]:
        res = []
        self.helper(root, res)
        return res

    def helper(self, root: TreeNode, res: List[int]):
        if root is not None:
            if root.left is not None:
                self.helper(root.left, res)
            res.append(root.val)
            if root.right is not None:
                self.helper(root.right, res)


class TestSolution(unittest.TestCase):
    def test_inorderTraversal(self):
        s = Solution()
        # Test case 1
        root1 = TreeNode(1)
        root1.right = TreeNode(2)
        root1.right.left = TreeNode(3)
        self.assertEqual(s.inorderTraversal(root1), [1,3,2])
        # Test case 2
        root2 = None
        self.assertEqual(s.inorderTraversal(root2), [])
        # Test case 3
        root3 = TreeNode(1)
        self.assertEqual(s.inorderTraversal(root3), [1])

if __name__ == '__main__':
    unittest.main()
