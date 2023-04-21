"""
Given the root of a binary tree, return the bottom-up level order traversal of its nodes' values.

(i.e., from left to right, level by level from leaf to root).
"""

from typing import List

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def levelOrderBottom(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return []
        
        queue = []
        result = []
        queue.append(root)
        
        while queue:
            level_size = len(queue)
            level = []
            for i in range(level_size):
                node = queue.pop(0)
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.insert(0, level)
        
        return result