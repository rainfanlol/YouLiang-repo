"""
Given two integer arrays inorder and postorder where inorder is the inorder traversal of a binary tree and postorder is the postorder traversal of the same tree,

construct and return the binary tree.
"""

from typing import List

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
def buildTree(inorder: List[int], postorder: List[int]) -> TreeNode:
    def helper(in_left, in_right):
        nonlocal post_idx
        if in_left > in_right:
            return None
        root_val = postorder[post_idx]
        root = TreeNode(root_val)
        index = idx_map[root_val]
        post_idx -= 1
        root.right = helper(index + 1, in_right)
        root.left = helper(in_left, index - 1)
        return root
    post_idx = len(postorder) - 1
    idx_map = {val:idx for idx, val in enumerate(inorder)}
    return helper(0, len(inorder) - 1)
if __name__ == "__main__":
    inorder = [9,3,15,20,7]
    postorder = [9,15,7,20,3]
    root = buildTree(inorder, postorder)
    assert root.val == 3
    assert root.left.val == 9
    assert root.right.val == 20
    assert root.right.left.val == 15
    assert root.right.right.val == 7
    inorder = [-1]
    postorder = [-1]
    root = buildTree(inorder, postorder)
    assert root.val == -1