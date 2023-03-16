"""
Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:

The left subtree of a node contains only nodes with keys less than the node's key.
The right subtree of a node contains only nodes with keys greater than the node's key.
Both the left and right subtrees must also be binary search trees.
"""

import unittest

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        return self.helper(root, None, None)
    
    def helper(self, node: TreeNode, min_val: int, max_val: int) -> bool:
        if node is None:
            return True
        if (min_val is not None and node.val <= min_val) or (max_val is not None and node.val >= max_val):
            return False
        left_valid = self.helper(node.left, min_val, node.val)
        right_valid = self.helper(node.right, node.val, max_val)
        return left_valid and right_valid

class TestSolution(unittest.TestCase):
    def test_isValidBST(self):
        root1 = TreeNode(2, TreeNode(1), TreeNode(3))
        root2 = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))
        root3 = TreeNode(1, TreeNode(1))
        s = Solution()
        self.assertEqual(s.isValidBST(root1), True)
        self.assertEqual(s.isValidBST(root2), False)
        self.assertEqual(s.isValidBST(root3), False)

if __name__ == '__main__':
    unittest.main()