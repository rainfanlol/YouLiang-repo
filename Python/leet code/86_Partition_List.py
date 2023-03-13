"""
Given the head of a linked list and a value x, partition it such that all nodes less than x come before nodes greater than or equal to x.

You should preserve the original relative order of the nodes in each of the two partitions.
"""
import unittest
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        dummy_small = ListNode()
        dummy_large = ListNode()
        small = dummy_small
        large = dummy_large
        
        current = head
        while current:
            if current.val < x:
                small.next = current
                small = small.next
            else:
                large.next = current
                large = large.next
            current = current.next
            
        large.next = None
        small.next = dummy_large.next
        
        return dummy_small.next



class TestSolution(unittest.TestCase):
    def test_example1(self):
        # Input: head = [1,4,3,2,5,2], x = 3
        # Output: [1,2,2,4,3,5]
        node1 = ListNode(1)
        node2 = ListNode(4)
        node3 = ListNode(3)
        node4 = ListNode(2)
        node5 = ListNode(5)
        node6 = ListNode(2)
        node1.next = node2
        node2.next = node3
        node3.next = node4
        node4.next = node5
        node5.next = node6
        s = Solution()
        result = s.partition(node1, 3)
        self.assertEqual(result.val, 1)
        self.assertEqual(result.next.val, 2)
        self.assertEqual(result.next.next.val, 2)
        self.assertEqual(result.next.next.next.val, 4)
        self.assertEqual(result.next.next.next.next.val, 3)
        self.assertEqual(result.next.next.next.next.next.val, 5)
        self.assertIsNone(result.next.next.next.next.next.next)
        
    def test_example2(self):
        # Input: head = [2,1], x = 2
        # Output: [1,2]
        node1 = ListNode(2)
        node2 = ListNode(1)
        node1.next = node2
        s = Solution()
        result = s.partition(node1, 2)
        self.assertEqual(result.val, 1)
        self.assertEqual(result.next.val, 2)
        self.assertIsNone(result.next.next)
        
    def test_empty_input(self):
        # Input: head = [], x = 0
        # Output: []
        s = Solution()
        result = s.partition(None, 0)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
