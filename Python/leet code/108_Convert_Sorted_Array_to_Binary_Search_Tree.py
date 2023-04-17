"""
Given an integer array nums where the elements are sorted in ascending order, convert it to a height-balanced binary search tree.
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def sortedArrayToBST(nums):
    def helper(l, r):
        if l > r:
            return None
        mid = (l + r) // 2
        node = TreeNode(nums[mid])
        node.left = helper(l, mid - 1)
        node.right = helper(mid + 1, r)
        return node
    return helper(0, len(nums) - 1)


if __name__ == "__main__":
    nums = [-10,-3,0,5,9]
    root = sortedArrayToBST(nums)
