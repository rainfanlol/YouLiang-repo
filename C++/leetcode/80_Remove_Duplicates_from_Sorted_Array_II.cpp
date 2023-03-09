/*
Given an integer array nums sorted in non-decreasing order, remove some duplicates in-place such that each unique element appears at most twice. The relative order of the elements should be kept the same.

Since it is impossible to change the length of the array in some languages, you must instead have the result be placed in the first part of the array nums. More formally, if there are k elements after removing the duplicates, then the first k elements of nums should hold the final result. It does not matter what you leave beyond the first k elements.

Return k after placing the final result in the first k slots of nums.

Do not allocate extra space for another array. You must do this by modifying the input array in-place with O(1) extra memory.
*/

#include <vector>
#include <cassert>

using namespace std;

int removeDuplicates(vector<int>& nums) {
    int n = nums.size();
    if (n <= 2) return n;
    int left = 2, right = 2;
    while (right < n) {
        if (nums[left - 2] != nums[right]) {
            nums[left] = nums[right];
            left++;
        }
        right++;
    }
    return left;
}

// 單元測試
int main() {
    vector<int> nums1 = {1,1,1,2,2,3};
    int expectedNums1[] = {1,1,2,2,3};
    int k1 = removeDuplicates(nums1);
    assert(k1 == 5);
    for (int i = 0; i < k1; i++) {
        assert(nums1[i] == expectedNums1[i]);
    }
    
    vector<int> nums2 = {0,0,1,1,1,1,2,3,3};
    int expectedNums2[] = {0,0,1,1,2,3,3};
    int k2 = removeDuplicates(nums2);
    assert(k2 == 7);
    for (int i = 0; i < k2; i++) {
        assert(nums2[i] == expectedNums2[i]);
    }
    
    return 0;
}
