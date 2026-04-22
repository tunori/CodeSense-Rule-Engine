def detect_algorithm(features: dict) -> dict:
    """
    Determines the algorithm pattern and category
    based on extracted structural features.
    """

    result = {
        "pattern": "Unknown",
        "category": "Unknown"
    }

    total_loops = features.get("for_loops", 0) + features.get("while_loops", 0)

    # ============================================================
    # Dynamic Programming
    # ============================================================

    if features.get("memoization_pattern"):
        return {
            "pattern": "Memoization",
            "category": "Dynamic Programming"
        }

    if features.get("tabulation_pattern"):
        return {
            "pattern": "Tabulation",
            "category": "Dynamic Programming"
        }

    # ============================================================
    # Heap-Based Algorithms
    # ============================================================

    if features.get("heap_pattern"):
        return {
            "pattern": "Heap-Based Algorithm",
            "category": "Data Structure Based"
        }

    # ============================================================
    # Search Algorithms
    # ============================================================

    if features.get("binary_search_pattern"):
        return {
            "pattern": "Binary Search",
            "category": "Search Algorithm"
        }

    # ============================================================
    # Graph Algorithms
    # ============================================================

    if features.get("bfs_pattern"):
        return {
            "pattern": "Breadth-First Search",
            "category": "Graph Algorithm"
        }

    if features.get("dfs_pattern"):
        return {
            "pattern": "Depth-First Search",
            "category": "Graph Algorithm"
        }

    # ============================================================
    # Pointer Techniques
    # ============================================================

    if features.get("sliding_window_pattern"):
        return {
            "pattern": "Sliding Window",
            "category": "Pointer Technique"
        }

    if (
        len(features.get("pointer_variables", [])) >= 2
        and features.get("pointer_updates", 0) >= 2
        and features.get("while_loops", 0) >= 1
    ):
        return {
            "pattern": "Two-Pointer Technique",
            "category": "Pointer Technique"
        }

    # ============================================================
    # Sorting Algorithms
    # ============================================================

    if features.get("bubble_sort_pattern"):
        return {
            "pattern": "Bubble Sort",
            "category": "Sorting Algorithm"
        }

    if features.get("insertion_sort_pattern"):
        return {
            "pattern": "Insertion Sort",
            "category": "Sorting Algorithm"
        }

    if features.get("merge_sort_pattern"):
        return {
            "pattern": "Merge Sort",
            "category": "Sorting Algorithm"
        }

    if features.get("quick_sort_pattern"):
        return {
            "pattern": "Quick Sort",
            "category": "Sorting Algorithm"
        }

    # ============================================================
    # Recursive Patterns
    # ============================================================

    if features.get("divide_and_conquer"):
        return {
            "pattern": "Recursive Divide-and-Conquer",
            "category": "Divide-and-Conquer"
        }

    if features.get("recursion") and features.get("recursive_call_count", 0) >= 2:
        return {
            "pattern": "Recursive (Exponential)",
            "category": "Recursive Pattern"
        }

    if features.get("recursion"):
        return {
            "pattern": "Recursive (Linear)",
            "category": "Recursive Pattern"
        }

    # ============================================================
    # Iterative Patterns
    # ============================================================

    if features.get("max_loop_depth", 0) >= 2:
        return {
            "pattern": "Nested Iterative",
            "category": "Iterative Pattern"
        }

    if total_loops == 1:
        return {
            "pattern": "Linear Iterative",
            "category": "Iterative Pattern"
        }

    if total_loops == 0:
        return {
            "pattern": "Constant-Time",
            "category": "Direct Computation"
        }

    return result