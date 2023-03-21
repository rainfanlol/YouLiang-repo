"""
Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).
"""

import unittest

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        if not root:
            return True
        return self.isMirror(root.left, root.right)
    
    def isMirror(self, left: TreeNode, right: TreeNode) -> bool:
        if not left and not right:
            return True
        if not left or not right:
            return False
        if left.val != right.val:
            return False
        return self.isMirror(left.left, right.right) and self.isMirror(left.right, right.left)
    

class TestSolution(unittest.TestCase):
    def test_isSymmetric(self):
        root1 = TreeNode(1, TreeNode(2, TreeNode(3), TreeNode(4)), TreeNode(2, TreeNode(4), TreeNode(3)))
        s = Solution()
        self.assertEqual(s.isSymmetric(root1), True)
        
        root2 = TreeNode(1, TreeNode(2, None, TreeNode(3)), TreeNode(2, None, TreeNode(3)))
        self.assertEqual(s.isSymmetric(root2), False)

if __name__ == '__main__':
    unittest.main()
