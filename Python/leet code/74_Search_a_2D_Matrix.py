"""
You are given an m x n integer matrix matrix with the following two properties:

Each row is sorted in non-decreasing order.
The first integer of each row is greater than the last integer of the previous row.
Given an integer target, return true if target is in matrix or false otherwise.

You must write a solution in O(log(m * n)) time complexity.
"""
import unittest

def search_matrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    l, r = 0, m * n - 1
    while l <= r:
        mid = (l + r) // 2
        mid_val = matrix[mid // n][mid % n]
        if mid_val == target:
            return True
        elif mid_val < target:
            l = mid + 1
        else:
            r = mid - 1
    return False

class TestSearchMatrix(unittest.TestCase):
    def test_example1(self):
        matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
        target = 3
        self.assertTrue(search_matrix(matrix, target))
        
    def test_example2(self):
        matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
        target = 13
        self.assertFalse(search_matrix(matrix, target))
        
    def test_single_element(self):
        matrix = [[1]]
        target = 1
        self.assertTrue(search_matrix(matrix, target))
        
    def test_single_element_not_found(self):
        matrix = [[1]]
        target = 2
        self.assertFalse(search_matrix(matrix, target))
        
    def test_row_not_found(self):
        matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
        target = 8
        self.assertFalse(search_matrix(matrix, target))
        
    def test_column_not_found(self):
        matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
        target = 13
        self.assertFalse(search_matrix(matrix, target))
        
if __name__ == '__main__':
    unittest.main()