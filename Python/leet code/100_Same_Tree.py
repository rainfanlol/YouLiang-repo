"""
Given the roots of two binary trees p and q, write a function to check if they are the same or not.

Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.
"""

import unittest

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def is_same_tree(p: TreeNode, q: TreeNode) -> bool:
    if not p and not q:
        return True
    if not p or not q:
        return False
    if p.val != q.val:
        return False
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)

class TestSameTree(unittest.TestCase):
    def test_example1(self):
        p = TreeNode(1, TreeNode(2), TreeNode(3))
        q = TreeNode(1, TreeNode(2), TreeNode(3))
        self.assertTrue(is_same_tree(p, q))

    def test_example2(self):
        p = TreeNode(1, TreeNode(2))
        q = TreeNode(1, None, TreeNode(2))
        self.assertFalse(is_same_tree(p, q))

    def test_example3(self):
        p = TreeNode(1, TreeNode(2), TreeNode(1))
        q = TreeNode(1, TreeNode(1), TreeNode(2))
        self.assertFalse(is_same_tree(p, q))

    def test_empty_tree(self):
        p = None
        q = None
        self.assertTrue(is_same_tree(p, q))

    def test_one_node_tree(self):
        p = TreeNode(1)
        q = TreeNode(1)
        self.assertTrue(is_same_tree(p, q))
        
if __name__ == '__main__':
    unittest.main()
