"""
Given the root of a binary tree, return the zigzag level order traversal of its nodes' values. (i.e., from left to right, then right to left for the next level and alternate between).
"""

import unittest

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def zigzagLevelOrder(self, root):
        if not root:
            return []
        
        result = []
        queue = [root]
        level = 0
        
        while queue:
            level_length = len(queue)
            level_values = []
            
            for i in range(level_length):
                node = queue.pop(0)
                level_values.append(node.val)
                
                if node.left:
                    queue.append(node.left)
                
                if node.right:
                    queue.append(node.right)
            
            if level % 2 == 1:
                level_values.reverse()
            
            result.append(level_values)
            level += 1
        
        return result

class TestSolution(unittest.TestCase):
    def test_example1(self):
        root = TreeNode(3)
        root.left = TreeNode(9)
        root.right = TreeNode(20)
        root.right.left = TreeNode(15)
        root.right.right = TreeNode(7)

        s = Solution()
        expected_output = [[3],[20,9],[15,7]]
        self.assertEqual(s.zigzagLevelOrder(root), expected_output)

    def test_example2(self):
        root = TreeNode(1)

        s = Solution()
        expected_output = [[1]]
        self.assertEqual(s.zigzagLevelOrder(root), expected_output)

    def test_example3(self):
        root = None

        s = Solution()
        expected_output = []
        self.assertEqual(s.zigzagLevelOrder(root), expected_output)

if __name__ == '__main__':
    unittest.main()
