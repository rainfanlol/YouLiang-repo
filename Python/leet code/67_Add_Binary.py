"""
Given two binary strings a and b, return their sum as a binary string.
"""
import unittest

class Solution:
    def addBinary(self,a: str, b: str) -> str:
        # 將a和b轉成int型態，並相加
        sum_int = int(a, 2) + int(b, 2)
        # 將相加的結果轉成二進制，並回傳字串
        return bin(sum_int)[2:]
    
class TestSolution(unittest.TestCase):
    def setUp(self):
        self.s = Solution()

    def test_example1(self):
        self.assertEqual(self.s.addBinary("1010", "1011"), "10101")

    def test_example2(self):
        self.assertEqual(self.s.addBinary("1111", "1111"), "11110")

if __name__ == '__main__':
    unittest.main()
