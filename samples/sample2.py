import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from analyzer import analyze_code

code_bfs = """
from collections import deque

def bfs(graph, start):
    queue = deque([start])
    visited = set()

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                queue.append(neighbor)
"""
print("CodeSense: ", analyze_code(code_bfs))