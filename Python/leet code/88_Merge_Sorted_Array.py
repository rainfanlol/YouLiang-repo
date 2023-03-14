"""
You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, and two integers m and n, representing the number of elements in nums1 and nums2 respectively.

Merge nums1 and nums2 into a single array sorted in non-decreasing order.

The final sorted array should not be returned by the function, but instead be stored inside the array nums1. 

To accommodate this, nums1 has a length of m + n, where the first m elements denote the elements that should be merged, 

and the last n elements are set to 0 and should be ignored. nums2 has a length of n.
"""

import unittest

class Solution:
    def merge(self, nums1, m, nums2, n):
        """
        Do not return anything, modify nums1 in-place instead.
        """
        i, j, k = m - 1, n - 1, m + n - 1
        while i >= 0 and j >= 0:
            if nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                i -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1
            k -= 1
        if j >= 0:
            nums1[:k+1] = nums2[:j+1]

class TestSolution(unittest.TestCase):
    def test_example1(self):
        s = Solution()
        nums1 = [1,2,3,0,0,0]
        nums2 = [2,5,6]
        m = 3
        n = 3
        s.merge(nums1, m, nums2, n)
        self.assertEqual(nums1, [1,2,2,3,5,6])

    def test_example2(self):
        s = Solution()
        nums1 = [1]
        nums2 = []
        m = 1
        n = 0
        s.merge(nums1, m, nums2, n)
        self.assertEqual(nums1, [1])

    def test_example3(self):
        s = Solution()
        nums1 = [0]
        nums2 = [1]
        m = 0
        n = 1
        s.merge(nums1, m, nums2, n)
        self.assertEqual(nums1, [1])

if __name__ == '__main__':
    unittest.main()