"""
You are given the root of a binary search tree (BST), where the values of exactly two nodes of the tree were swapped by mistake. Recover the tree without changing its structure.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def recoverTree(self, root: TreeNode) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        if not root:
            return
        
        x = y = prev = pred = None
        while root:
            if root.left:
                pred = root.left
                while pred.right and pred.right != root:
                    pred = pred.right
                if not pred.right:
                    pred.right = root
                    root = root.left
                else:
                    if prev and root.val < prev.val:
                        y = root
                        if not x:
                            x = prev
                    prev = root
                    pred.right = None
                    root = root.right
            else:
                if prev and root.val < prev.val:
                    y = root
                    if not x:
                        x = prev
                prev = root
                root = root.right
        
        x.val, y.val = y.val, x.val



