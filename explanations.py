def generate_explanation(analysis_result: dict) -> dict:
    """
    Generates structured explanations.

    Priority:
    1. Detected algorithm pattern
    2. Strong structural features
    3. Generic fallback
    """

    features = analysis_result.get("features", {})
    pattern = analysis_result.get("analysis", {}).get("pattern")

    explanation = ""

    # ============================================================
    # Pattern-Based Explanations
    # ============================================================

    if pattern == "Quick Sort":
        explanation = "Quick Sort: Uses a pivot to partition and recursively sort subarrays."

    elif pattern == "Merge Sort":
        explanation = "Merge Sort: Recursively splits and merges sorted halves."

    elif pattern == "Bubble Sort":
        explanation = "Bubble Sort: Repeated adjacent swaps push larger elements to the end."

    elif pattern == "Insertion Sort":
        explanation = "Insertion Sort: Inserts elements into a growing sorted portion."

    elif pattern in ("Heap-Based Algorithm", "Heap Sort"):
        explanation = "Heap-based approach: Maintains ordered elements using a priority structure."

    elif pattern == "Breadth-First Search":
        explanation = "BFS: Explores nodes level by level using a queue."

    elif pattern == "Depth-First Search":
        explanation = "DFS: Explores deeply along branches before backtracking."

    elif pattern == "Binary Search":
        explanation = "Binary Search: Repeatedly halves the search space."

    elif pattern == "Memoization":
        explanation = "Memoization: Caches results to avoid redundant computation."

    elif pattern == "Tabulation":
        explanation = "Tabulation: Builds solutions iteratively using a DP table."

    elif pattern == "Sliding Window":
        explanation = "Sliding Window: Expands and shrinks a window over data efficiently."

    elif pattern == "Two-Pointer Technique":
        explanation = "Two-pointer: Two indices move in coordination during traversal."

    # ============================================================
    # Feature-Based Fallback
    # ============================================================

    elif features.get("heap_pattern"):
        explanation = "Heap operations detected."

    elif features.get("memoization_pattern"):
        explanation = "Memoization behavior detected."

    elif features.get("tabulation_pattern"):
        explanation = "Tabulation-based DP detected."

    elif features.get("bfs_pattern"):
        explanation = "BFS-like traversal detected."

    elif features.get("dfs_pattern"):
        explanation = "DFS-like traversal detected."

    elif features.get("binary_search_pattern"):
        explanation = "Binary search pattern detected."

    elif features.get("sliding_window_pattern"):
        explanation = "Sliding window behavior detected."

    elif features.get("pointer_updates", 0) >= 2:
        explanation = "Two-pointer behavior detected."

    elif features.get("merge_sort_pattern"):
        explanation = "Merge sort structure detected."

    elif features.get("quick_sort_pattern"):
        explanation = "Quick sort structure detected."

    elif features.get("divide_and_conquer"):
        explanation = "Divide-and-conquer approach detected."

    elif features.get("recursion") and features.get("recursive_call_count", 0) > 1:
        explanation = "Multiple recursive calls suggest exponential growth."

    elif features.get("recursion"):
        explanation = "Single recursion chain detected."

    elif features.get("max_loop_depth", 0) > 1:
        explanation = "Nested loops indicate polynomial complexity."

    elif features.get("max_loop_depth", 0) == 1:
        explanation = "Single loop indicates linear behavior."

    else:
        explanation = "No strong structural pattern detected."

    return {
        "summary": explanation,
        "details": [explanation]
    }