/*
There is an integer array nums sorted in non-decreasing order (not necessarily with distinct values).

Before being passed to your function, nums is rotated at an unknown pivot index k (0 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). 

For example, [0,1,2,4,4,4,5,6,6,7] might be rotated at pivot index 5 and become [4,5,6,6,7,0,1,2,4,4].

Given the array nums after the rotation and an integer target, return true if target is in nums, or false if it is not in nums.

You must decrease the overall operation steps as much as possible.
*/

#include <vector>
#include <cassert>

using namespace std;

class Solution {
public:
    bool search(vector<int>& nums, int target) {
        int n = nums.size();
        int left = 0, right = n - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) return true;

            if (nums[left] < nums[mid]) {  // left half is sorted
                if (nums[left] <= target && target < nums[mid]) {
                    right = mid - 1;
                } else {
                    left = mid + 1;
                }
            } else if (nums[left] > nums[mid]) {  // right half is sorted
                if (nums[mid] < target && target <= nums[right]) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            } else {  // nums[left] == nums[mid]
                left++;
            }
        }

        return false;
    }
};

int main() {
    Solution s;

    vector<int> nums1 = {1, 3, 5, 7, 9};
    assert(s.search(nums1, 5));
    assert(!s.search(nums1, 6));

    vector<int> nums2 = {5, 7, 9, 1, 3};
    assert(s.search(nums2, 3));
    assert(!s.search(nums2, 4));

    vector<int> nums3 = {1};
    assert(s.search(nums3, 1));
    assert(!s.search(nums3, 0));

    vector<int> nums4 = {1, 0, 1, 1, 1};
    assert(s.search(nums4, 0));
    assert(s.search(nums4, 1));
    assert(!s.search(nums4, 2));

    return 0;
}


