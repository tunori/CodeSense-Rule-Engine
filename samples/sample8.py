import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from analyzer import analyze_code

code_window = """
def max_sum(arr, k):
    left = 0
    current_sum = 0
    max_sum = 0

    for right in range(len(arr)):
        current_sum += arr[right]

        while right - left + 1 > k:
            current_sum -= arr[left]
            left += 1

        max_sum = max(max_sum, current_sum)

    return max_sum
"""
print("CodeSense:", analyze_code(code_window))