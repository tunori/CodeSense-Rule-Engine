import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from analyzer import analyze_code

code_two_pointer = """
def two_sum(arr, target):
    left, right = 0, len(arr)-1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return True
        elif s < target:
            left += 1
        else:
            right -= 1
"""
print("CodeSense:", analyze_code(code_two_pointer))