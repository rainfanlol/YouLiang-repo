"""
Given the head of a singly linked list and two integers left and right where left <= right, 

reverse the nodes of the list from position left to position right, and return the reversed list.
"""

import unittest

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    @staticmethod
    def reverse_between(head: ListNode, left: int, right: int) -> ListNode:
        if not head or left == right:
            return head
        
        dummy = ListNode(0)
        dummy.next = head
        pre = dummy

        for i in range(left - 1):
            pre = pre.next

        cur = pre.next
        for i in range(right - left):
            nxt = cur.next
            cur.next = nxt.next
            nxt.next = pre.next
            pre.next = nxt

        return dummy.next



class TestSolution(unittest.TestCase):
    def createLinkedList(self, arr):
        head = ListNode(0)
        cur = head
        for val in arr:
            cur.next = ListNode(val)
            cur = cur.next
        return head.next

    def linkedListToArray(self, head):
        arr = []
        while head:
            arr.append(head.val)
            head = head.next
        return arr

    def test_reverse_between(self):
        s = Solution()
        head = self.createLinkedList([1, 2, 3, 4, 5])
        left = 2
        right = 4
        expected = [1, 4, 3, 2, 5]
        actual = s.reverse_between(head, left, right)
        self.assertEqual(self.linkedListToArray(actual), expected)

        head = self.createLinkedList([5])
        left = 1
        right = 1
        expected = [5]
        actual = s.reverse_between(head, left, right)
        self.assertEqual(self.linkedListToArray(actual), expected)


if __name__ == "__main__":
    unittest.main()
