/*
Given an m x n grid of characters board and a string word, return true if word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.
*/

#include <vector>
#include <string>
#include <iostream>

using namespace std;

class Solution {
public:
    bool exist(vector<vector<char>>& board, string word) {
        if (board.empty() || board[0].empty()) return false;
        m = board.size(), n = board[0].size();
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                if (dfs(board, word, i, j, 0)) return true;
            }
        }
        return false;
    }
private:
    int m, n;
    bool dfs(vector<vector<char>>& board, string& word, int i, int j, int k) {
        if (i < 0 || i >= m || j < 0 || j >= n || board[i][j] != word[k]) return false;
        if (k == word.size() - 1) return true;
        char tmp = board[i][j];
        board[i][j] = '/';
        bool res = dfs(board, word, i + 1, j, k + 1) || dfs(board, word, i - 1, j, k + 1) || dfs(board, word, i, j + 1, k + 1) || dfs(board, word, i, j - 1, k + 1);
        board[i][j] = tmp;
        return res;
    }
};

int main() {
    Solution sol;
    vector<vector<char>> board = {{'A','B','C','E'},{'S','F','C','S'},{'A','D','E','E'}};
    string word1 = "ABCCED";
    string word2 = "SEE";
    string word3 = "ABCB";
    cout << boolalpha << sol.exist(board, word1) << endl; // expected output: true
    cout << boolalpha << sol.exist(board, word2) << endl; // expected output: true
    cout << boolalpha << sol.exist(board, word3) << endl; // expected output: false
    return 0;
}
