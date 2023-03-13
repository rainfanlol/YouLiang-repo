"""
Given the head of a sorted linked list, delete all duplicates such that each element appears only once. Return the linked list sorted as well.
"""

import unittest
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return None
        
        current = head
        while current.next:
            if current.val == current.next.val:
                current.next = current.next.next
            else:
                current = current.next
                
        return head


class TestSolution(unittest.TestCase):
    def test_example1(self):
        # Input: head = [1,1,2]
        # Output: [1,2]
        node1 = ListNode(1)
        node2 = ListNode(1)
        node3 = ListNode(2)
        node1.next = node2
        node2.next = node3
        s = Solution()
        result = s.deleteDuplicates(node1)
        self.assertEqual(result.val, 1)
        self.assertEqual(result.next.val, 2)
        self.assertIsNone(result.next.next)
        
    def test_example2(self):
        # Input: head = [1,1,2,3,3]
        # Output: [1,2,3]
        node1 = ListNode(1)
        node2 = ListNode(1)
        node3 = ListNode(2)
        node4 = ListNode(3)
        node5 = ListNode(3)
        node1.next = node2
        node2.next = node3
        node3.next = node4
        node4.next = node5
        s = Solution()
        result = s.deleteDuplicates(node1)
        self.assertEqual(result.val, 1)
        self.assertEqual(result.next.val, 2)
        self.assertEqual(result.next.next.val, 3)
        self.assertIsNone(result.next.next.next)
        
    def test_empty_input(self):
        # Input: head = []
        # Output: []
        s = Solution()
        result = s.deleteDuplicates(None)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)