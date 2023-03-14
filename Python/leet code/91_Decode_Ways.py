"""
A message containing letters from A-Z can be encoded into numbers using the following mapping:

'A' -> "1"
'B' -> "2"
...
'Z' -> "26"
To decode an encoded message, all the digits must be grouped then mapped back into letters using the reverse of the mapping above (there may be multiple ways). For example, "11106" can be mapped into:

"AAJF" with the grouping (1 1 10 6)
"KJF" with the grouping (11 10 6)
Note that the grouping (1 11 06) is invalid because "06" cannot be mapped into 'F' since "6" is different from "06".

Given a string s containing only digits, return the number of ways to decode it.

The test cases are generated so that the answer fits in a 32-bit integer.
"""

import unittest

class Solution:
    def numDecodings(self, s: str) -> int:
        if not s or s[0] == '0':
            return 0
        
        n = len(s)
        dp = [0] * (n + 1)
        dp[0], dp[1] = 1, 1
        
        for i in range(2, n + 1):
            if s[i-1] != '0':
                dp[i] += dp[i-1]
            
            if s[i-2] == '1' or (s[i-2] == '2' and s[i-1] <= '6'):
                dp[i] += dp[i-2]
                
        return dp[n]
    
class TestSolution(unittest.TestCase):
    def test_example1(self):
        s = Solution()
        self.assertEqual(s.numDecodings("12"), 2)

    def test_example2(self):
        s = Solution()
        self.assertEqual(s.numDecodings("226"), 3)

    def test_example3(self):
        s = Solution()
        self.assertEqual(s.numDecodings("06"), 0)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
