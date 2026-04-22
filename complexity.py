def estimate_complexity(features: dict) -> dict:
    """
    Estimates time complexity using heuristic rules
    based on extracted structural features.
    """

    result = {
        "time_complexity": "O(1)",
        "explanation": "No loops or recursion detected."
    }

    max_depth = features.get("max_loop_depth", 0)

    # ============================================================
    # Graph Algorithms
    # ============================================================

    if features.get("bfs_pattern") or features.get("dfs_pattern"):
        return {
            "time_complexity": "O(V + E)",
            "explanation": "Graph traversal visits nodes and edges."
        }

    # ============================================================
    # Search Algorithms
    # ============================================================

    if features.get("binary_search_pattern"):
        return {
            "time_complexity": "O(log n)",
            "explanation": "Search space is halved each iteration."
        }

    # ============================================================
    # Dynamic Programming
    # ============================================================

    if features.get("dp_pattern"):
        return {
            "time_complexity": "O(n) or O(n²)",
            "explanation": "Depends on number of states and transitions."
        }

    # ============================================================
    # Sorting Algorithms
    # ============================================================

    if features.get("merge_sort_pattern"):
        return {
            "time_complexity": "O(n log n)",
            "explanation": "Divide-and-conquer with linear merge step."
        }

    if features.get("quick_sort_pattern"):
        return {
            "time_complexity": "O(n log n) average, O(n²) worst-case",
            "explanation": "Partition-based recursive sorting."
        }

    if features.get("bubble_sort_pattern"):
        return {
            "time_complexity": "O(n²)",
            "explanation": "Nested iteration with repeated swaps."
        }

    if features.get("insertion_sort_pattern"):
        return {
            "time_complexity": "O(n²)",
            "explanation": "Element shifting within sorted portion."
        }

    # ============================================================
    # Recursion
    # ============================================================

    if features.get("recursion"):

        if features.get("divide_and_conquer"):
            return {
                "time_complexity": "O(n log n)",
                "explanation": "Divide-and-conquer recursion."
            }

        if features.get("recursive_call_count", 0) >= 2:
            return {
                "time_complexity": "O(2^n)",
                "explanation": "Multiple recursive branches."
            }

        return {
            "time_complexity": "O(n)",
            "explanation": "Single recursive chain."
        }

    # ============================================================
    # Other Patterns
    # ============================================================

    if features.get("sliding_window_pattern"):
        return {
            "time_complexity": "O(n)",
            "explanation": "Window moves linearly across data."
        }

    if features.get("heap_pattern"):
        return {
            "time_complexity": "O(n log n) or O(log n) per operation",
            "explanation": "Heap operations are logarithmic."
        }

    # ============================================================
    # Iterative Fallback
    # ============================================================

    if max_depth == 1:
        return {
            "time_complexity": "O(n)",
            "explanation": "Single loop traversal."
        }

    if max_depth >= 2:
        return {
            "time_complexity": f"O(n^{max_depth})",
            "explanation": "Nested loops increase polynomial complexity."
        }

    return result