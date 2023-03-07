"""
You are given a large integer represented as an integer array digits, where each digits[i] is the ith digit of the integer. 
The digits are ordered from most significant to least significant in left-to-right order. 
The large integer does not contain any leading 0's.
Increment the large integer by one and return the resulting array of digits.
"""

import unittest

class Solution:
    def plus_one(digits):
        # Start from the least significant digit
        for i in range(len(digits)-1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1
                return digits
            else:
                digits[i] = 0
        # Create a new array if there is a carry at the most significant digit
        return [1] + [0] * len(digits)
    

class TestPlusOne(unittest.TestCase):
    
    def test_normal_case(self):
        self.assertEqual(Solution.plus_one([1, 2, 3]), [1, 2, 4])
        self.assertEqual(Solution.plus_one([4, 3, 2, 1]), [4, 3, 2, 2])
        self.assertEqual(Solution.plus_one([9]), [1, 0])
        
    def test_edge_case(self):
        self.assertEqual(Solution.plus_one([0]), [1])
    
if __name__ == '__main__':

    digits = [1, 2, 3]
    result = Solution.plus_one(digits)
    print(result)

    digits = [4, 3, 2, 1]
    result = Solution.plus_one(digits)
    print(result)

    digits = [9]
    result = Solution.plus_one(digits)
    print(result)

    unittest.main()
