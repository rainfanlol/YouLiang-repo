"""
Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).
"""

from typing import List
from collections import deque
import unittest

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return []
        result = []
        queue = deque([root])
        while queue:
            level_size = len(queue)
            current_level = []
            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(current_level)
        return result

class TestSolution(unittest.TestCase):
    def test_levelOrder(self):
        root1 = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
        s = Solution()
        self.assertEqual(s.levelOrder(root1), [[3], [9, 20], [15, 7]])
        
        root2 = TreeNode(1)
        self.assertEqual(s.levelOrder(root2), [[1]])
        
        self.assertEqual(s.levelOrder(None), [])

if __name__ == '__main__':
    unittest.main()
