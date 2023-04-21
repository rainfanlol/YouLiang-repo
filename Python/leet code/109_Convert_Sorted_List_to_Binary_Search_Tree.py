"""
Given the head of a singly linked list where elements are sorted in ascending order, convert it to a height-balanced binary search tree.
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
class Solution:
    def sortedListToBST(self, head: ListNode) -> TreeNode:
        if not head:
            return None
        if not head.next:
            return TreeNode(head.val)
        # 使用快慢指針找到中間節點，將其作為根節點
        slow, fast = head, head.next.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        mid = slow.next
        slow.next = None
        
        # 將左半部分轉換為BST，連接到根節點
        root = TreeNode(mid.val)
        root.left = self.sortedListToBST(head)
        # 將右半部分轉換為BST，連接到根節點
        root.right = self.sortedListToBST(mid.next)
        return root