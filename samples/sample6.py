import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from analyzer import analyze_code

code_quick = """
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x <= pivot]
    right = [x for x in arr[1:] if x > pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)
"""
print("CodeSense:", analyze_code(code_quick))