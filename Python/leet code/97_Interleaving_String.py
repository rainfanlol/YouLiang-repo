"""
Given strings s1, s2, and s3, find whether s3 is formed by an interleaving of s1 and s2.

An interleaving of two strings s and t is a configuration where s and t are divided into n and m 
substrings
 respectively, such that:

s = s1 + s2 + ... + sn
t = t1 + t2 + ... + tm
|n - m| <= 1
The interleaving is s1 + t1 + s2 + t2 + s3 + t3 + ... or t1 + s1 + t2 + s2 + t3 + s3 + ...
Note: a + b is the concatenation of strings a and b.
"""
import unittest

def isInterleave(s1: str, s2: str, s3: str) -> bool:
    n, m = len(s1), len(s2)
    if len(s3) != n + m:
        return False
    dp = [False] * (m+1)
    for i in range(n+1):
        for j in range(m+1):
            if i == 0 and j == 0:
                dp[j] = True
            elif i == 0:
                dp[j] = dp[j-1] and s2[j-1] == s3[j-1]
            elif j == 0:
                dp[j] = dp[j] and s1[i-1] == s3[i-1]
            else:
                dp[j] = (dp[j] and s1[i-1] == s3[i+j-1]) or (dp[j-1] and s2[j-1] == s3[i+j-1])
    return dp[m]

class TestSolution(unittest.TestCase):
    def test_example1(self):
        s1, s2, s3 = "aabcc", "dbbca", "aadbbcbcac"
        self.assertTrue(isInterleave(s1, s2, s3))

    def test_example2(self):
        s1, s2, s3 = "aabcc", "dbbca", "aadbbbaccc"
        self.assertFalse(isInterleave(s1, s2, s3))

    def test_example3(self):
        s1, s2, s3 = "", "", ""
        self.assertTrue(isInterleave(s1, s2, s3))

if __name__ == '__main__':
    unittest.main()
