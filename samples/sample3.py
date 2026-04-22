import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from analyzer import analyze_code

code_dfs = """
def dfs(graph, node, visited):
    if node in visited:
        return
    visited.add(node)

    for neighbor in graph[node]:
        dfs(graph, neighbor, visited)
"""
print("CodeSense:", analyze_code(code_dfs))