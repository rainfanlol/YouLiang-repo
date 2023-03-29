"""
Given two integer arrays preorder and inorder where preorder is the preorder traversal of a binary tree and inorder is the inorder traversal of the same tree, 

construct and return the binary tree.
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def buildTree(preorder, inorder):
    if not preorder or not inorder:
        return None
    root_val = preorder.pop(0)
    root = TreeNode(root_val)
    idx = inorder.index(root_val)
    root.left = buildTree(preorder, inorder[:idx])
    root.right = buildTree(preorder, inorder[idx+1:])
    return root



