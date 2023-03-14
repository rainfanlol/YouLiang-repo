/*
A valid IP address consists of exactly four integers separated by single dots. Each integer is between 0 and 255 (inclusive) and cannot have leading zeros.

For example, "0.1.2.201" and "192.168.1.1" are valid IP addresses, but "0.011.255.245", "192.168.1.312" and "192.168@1.1" are invalid IP addresses.

Given a string s containing only digits, return all possible valid IP addresses that can be formed by inserting dots into s. 

You are not allowed to reorder or remove any digits in s. You may return the valid IP addresses in any order.
*/

#include <vector>
#include <string>
#include <cassert>

using namespace std;

class Solution {
public:
    vector<string> restoreIpAddresses(string s) {
        vector<string> res;
        if (s.length() < 4 || s.length() > 12) {
            return res;
        }
        string temp;
        restore(s, 0, 0, temp, res);
        return res;
    }

    void restore(string s, int index, int count, string temp, vector<string>& res) {
        if (count > 4) {
            return;
        }
        if (count == 4 && index == s.length()) {
            res.push_back(temp);
            return;
        }
        for (int i = 1; i < 4; i++) {
            if (index + i > s.length()) {
                break;
            }
            string str = s.substr(index, i);
            if ((str[0] == '0' && str.length() > 1) || stoi(str) > 255) {
                continue;
            }
            restore(s, index + i, count + 1, temp + str + (count == 3 ? "" : "."), res);
        }
    }
};


int main() {
    Solution s;

    vector<string> res = s.restoreIpAddresses("25525511135");
    vector<string> expected = {"255.255.11.135", "255.255.111.35"};
    assert(res == expected);

    res = s.restoreIpAddresses("0000");
    expected = {"0.0.0.0"};
    assert(res == expected);

    res = s.restoreIpAddresses("101023");
    expected = {"1.0.10.23", "1.0.102.3", "10.1.0.23", "10.10.2.3", "101.0.2.3"};
    assert(res == expected);

    return 0;
}