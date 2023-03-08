"""
Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.

We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.

You must solve this problem without using the library's sort function.
"""

import unittest

def sortColors(nums):
    """
    Do not return anything, modify nums in-place instead.
    """
    # 計算0、1、2的出現次數
    count_0, count_1, count_2 = 0, 0, 0
    for num in nums:
        if num == 0:
            count_0 += 1
        elif num == 1:
            count_1 += 1
        else:
            count_2 += 1
    
    # 修改nums的值
    for i in range(len(nums)):
        if i < count_0:
            nums[i] = 0
        elif i < count_0 + count_1:
            nums[i] = 1
        else:
            nums[i] = 2



class TestSortColors(unittest.TestCase):

    def test_example1(self):
        nums = [2, 0, 2, 1, 1, 0]
        sortColors(nums)
        self.assertEqual(nums, [0, 0, 1, 1, 2, 2])

    def test_example2(self):
        nums = [2, 0, 1]
        sortColors(nums)
        self.assertEqual(nums, [0, 1, 2])

if __name__ == '__main__':
    unittest.main()