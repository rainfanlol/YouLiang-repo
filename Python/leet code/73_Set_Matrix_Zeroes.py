"""
Given an m x n integer matrix matrix, if an element is 0, set its entire row and column to 0's.

You must do it in place.
"""
import unittest

class Solution:
    def setZeroes(self, matrix):
        """
        Do not return anything, modify matrix in-place instead.
        """
        m = len(matrix)
        n = len(matrix[0])
        first_col_has_zero = False
        
        # Step 1: Mark which rows and columns should be set to 0
        for i in range(m):
            if matrix[i][0] == 0:
                first_col_has_zero = True
                
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0
        
        # Step 2: Set elements to 0 for rows and columns marked in Step 1
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0
        
        # Step 3: Set elements in first row and first column to 0 if needed
        if matrix[0][0] == 0:
            for j in range(n):
                matrix[0][j] = 0
                
        if first_col_has_zero:
            for i in range(m):
                matrix[i][0] = 0

class TestSolution(unittest.TestCase):
    def test_example1(self):
        matrix = [[1,1,1],[1,0,1],[1,1,1]]
        expected_output = [[1,0,1],[0,0,0],[1,0,1]]
        Solution().setZeroes(matrix)
        self.assertEqual(matrix, expected_output)
        
    def test_example2(self):
        matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
        expected_output = [[0,0,0,0],[0,4,5,0],[0,3,1,0]]
        Solution().setZeroes(matrix)
        self.assertEqual(matrix, expected_output)
        
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)