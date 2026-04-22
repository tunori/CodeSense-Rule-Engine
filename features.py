import ast


class FeatureExtractor(ast.NodeVisitor):
    """
    Traverses the AST and extracts structural features
    from Python source code for algorithm pattern detection.
    """

    def __init__(self):
        # ===============================
        # Core Structural Features
        # ===============================
        self.features = {
            "for_loops": 0,
            "while_loops": 0,
            "function_calls": set(),
            "recursion": False,
            "recursive_call_count": 0,
            "max_loop_depth": 0,

            # ===============================
            # Divide & Conquer / Search
            # ===============================
            "divide_and_conquer": False,
            "binary_search_pattern": False,

            # ===============================
            # Pointer Techniques
            # ===============================
            "pointer_variables": set(),
            "pointer_updates": 0,

            # ===============================
            # Graph Traversal
            # ===============================
            "bfs_pattern": False,
            "dfs_pattern": False,
            "graph_iteration": False,

            # BFS-specific
            "queue_variables": set(),
            "queue_operations": 0,
            "queue_pop_front": False,
            "queue_append_detected": False,

            # DFS-specific
            "uses_stack": False,
            "uses_pop": False,

            # ===============================
            # Dynamic Programming
            # ===============================
            "dp_pattern": False,
            "uses_dp_array": False,
            "dp_self_dependency": False,
            "dp_dimension": 1,

            # Memoization
            "memoization_pattern": False,
            "memo_dict_defined": False,
            "memo_lookup_detected": False,
            "memo_store_detected": False,

            # Tabulation
            "tabulation_pattern": False,

            # ===============================
            # Sorting
            # ===============================
            "sorting_pattern": False,
            "bubble_sort_pattern": False,
            "insertion_sort_pattern": False,
            "merge_sort_pattern": False,
            "quick_sort_pattern": False,
            "adjacent_swap_detected": False,
            "insertion_shift_detected": False,

            # ===============================
            # Sliding Window
            # ===============================
            "sliding_window_pattern": False,
            "window_updates": 0,
            "window_shrinks": 0,

            # ===============================
            # Heap
            # ===============================
            "heap_imported": False,
            "heap_operations": 0,
            "heap_pattern": False,
        }

        self.current_function_name = None
        self.current_loop_depth = 0
        self.max_loop_depth = 0

    # ============================================================
    # Imports
    # ============================================================

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == "heapq":
                self.features["heap_imported"] = True
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module == "heapq":
            self.features["heap_imported"] = True
        self.generic_visit(node)

    # ============================================================
    # Function Tracking
    # ============================================================

    def visit_FunctionDef(self, node):
        previous = self.current_function_name
        self.current_function_name = node.name

        self.generic_visit(node)

        self.current_function_name = previous

        # Detect memo dict in function parameters
        for arg in node.args.defaults:
            if isinstance(arg, ast.Dict):
                self.features["memo_dict_defined"] = True

    # ============================================================
    # Loop Tracking
    # ============================================================

    def visit_For(self, node):
        self.features["for_loops"] += 1

        self.current_loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.current_loop_depth)

        # Heuristic: graph[node] iteration
        if isinstance(node.iter, ast.Subscript):
            self.features["graph_iteration"] = True

        self.generic_visit(node)
        self.current_loop_depth -= 1

        # Sliding window right pointer heuristic
        if isinstance(node.target, ast.Name):
            if node.target.id.lower() in ("right", "r", "end"):
                self.features["window_updates"] += 1

    def visit_While(self, node):
        self.features["while_loops"] += 1

        self.current_loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.current_loop_depth)

        self.generic_visit(node)
        self.current_loop_depth -= 1

    # ============================================================
    # Function Calls
    # ============================================================

    def visit_Call(self, node):
        # ---------- Direct function calls ----------
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            self.features["function_calls"].add(func_name)

            # Recursion detection
            if func_name == self.current_function_name:
                self.features["recursion"] = True
                self.features["recursive_call_count"] += 1

                # DFS heuristic
                if self.features["for_loops"] >= 1:
                    self.features["dfs_pattern"] = True

                # Divide & conquer detection
                for arg in node.args:
                    if isinstance(arg, ast.BinOp) and isinstance(arg.op, (ast.Div, ast.FloorDiv)):
                        self.features["divide_and_conquer"] = True

                    if isinstance(arg, ast.Subscript) and isinstance(arg.slice, ast.Slice):
                        self.features["divide_and_conquer"] = True
                        self.features["merge_sort_pattern"] = True

        # ---------- Method calls ----------
        if isinstance(node.func, ast.Attribute):
            method = node.func.attr

            # Queue operations
            if isinstance(node.func.value, ast.Name):
                var = node.func.value.id

                if var in self.features["queue_variables"]:
                    if method in ("append", "popleft"):
                        self.features["queue_operations"] += 1

            # Stack / pop detection
            if method == "pop":
                self.features["uses_pop"] = True

                if node.args and isinstance(node.args[0], ast.Constant):
                    if node.args[0].value == 0:
                        self.features["queue_pop_front"] = True

            if method == "append":
                self.features["queue_append_detected"] = True

            if method == "popleft":
                self.features["queue_pop_front"] = True

            # Heap operations
            if isinstance(node.func.value, ast.Name):
                if node.func.value.id == "heapq":
                    if method in ("heappush", "heappop", "heapify"):
                        self.features["heap_operations"] += 1

        # Iterative DFS heuristic
        if (
            self.features["uses_stack"]
            and self.features["uses_pop"]
            and self.features["for_loops"] >= 1
        ):
            self.features["dfs_pattern"] = True

        self.generic_visit(node)

    # ============================================================
    # Assignments
    # ============================================================

    def visit_Assign(self, node):

        # ---------- Binary Search ----------
        if isinstance(node.value, ast.BinOp) and isinstance(node.value.op, ast.FloorDiv):
            if isinstance(node.value.left, ast.BinOp) and isinstance(node.value.left.op, ast.Add):
                self.features["binary_search_pattern"] = True

        # ---------- Pointer Detection ----------
        if node.targets and isinstance(node.targets[0], ast.Name):
            var = node.targets[0].id

            if isinstance(node.value, (ast.Constant, ast.Num, ast.BinOp)):
                self.features["pointer_variables"].add(var)

        # ---------- BFS Queue ----------
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
            if node.value.func.id == "deque":
                if node.targets and isinstance(node.targets[0], ast.Name):
                    self.features["queue_variables"].add(node.targets[0].id)

        # ---------- Stack ----------
        if node.targets and isinstance(node.targets[0], ast.Name):
            var = node.targets[0].id.lower()
            if var == "stack" and isinstance(node.value, (ast.List, ast.Call)):
                self.features["uses_stack"] = True

        # ---------- Memoization ----------
        if isinstance(node.value, ast.Dict):
            if node.targets and isinstance(node.targets[0], ast.Name):
                if node.targets[0].id.lower() in ("memo", "cache", "dp"):
                    self.features["memo_dict_defined"] = True

        # memo[...] = ...
        if node.targets and isinstance(node.targets[0], ast.Subscript):
            base = node.targets[0].value
            if isinstance(base, ast.Name):
                if base.id.lower() in ("memo", "cache", "dp"):
                    self.features["memo_store_detected"] = True

        # ---------- DP Dimension ----------
        if isinstance(node.value, ast.ListComp):
            self.features["dp_dimension"] = 2

        if isinstance(node.value, ast.List):
            if any(isinstance(el, ast.List) for el in node.value.elts):
                self.features["dp_dimension"] = 2

        # ---------- DP Self Dependency ----------
        if node.targets and isinstance(node.targets[0], ast.Subscript):
            base = node.targets[0].value
            while isinstance(base, ast.Subscript):
                base = base.value

            if isinstance(base, ast.Name):
                var = base.id.lower()
                if var in ("dp", "memo", "cache"):
                    for child in ast.walk(node.value):
                        if isinstance(child, ast.Name) and child.id.lower() == var:
                            self.features["dp_self_dependency"] = True

        # ---------- Sorting ----------
        if (
            isinstance(node.targets[0], ast.Tuple)
            and isinstance(node.value, ast.Tuple)
            and len(node.targets[0].elts) == 2
            and len(node.value.elts) == 2
        ):
            if all(isinstance(el, ast.Subscript) for el in node.targets[0].elts + node.value.elts):
                self.features["adjacent_swap_detected"] = True

        if node.targets and isinstance(node.targets[0], ast.Subscript):
            if isinstance(node.value, ast.Subscript):
                self.features["insertion_shift_detected"] = True

        # Quick sort heuristic
        if node.targets and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id.lower() == "pivot":
                self.features["quick_sort_pattern"] = True

        self.generic_visit(node)

    # ============================================================
    # Augmented Assignments
    # ============================================================

    def visit_AugAssign(self, node):
        if isinstance(node.target, ast.Name):
            var = node.target.id

            if isinstance(node.op, (ast.Add, ast.Sub)):
                if var in self.features["pointer_variables"]:
                    self.features["pointer_updates"] += 1

            if var.lower() in ("left", "l", "start"):
                self.features["window_shrinks"] += 1

        self.generic_visit(node)

    # ============================================================
    # Subscript Access (DP usage)
    # ============================================================

    def visit_Subscript(self, node):
        base = node.value
        while isinstance(base, ast.Subscript):
            base = base.value

        if isinstance(base, ast.Name):
            if base.id.lower() in ("dp", "memo", "cache"):
                self.features["uses_dp_array"] = True

        self.generic_visit(node)

    # ============================================================
    # Comparisons
    # ============================================================

    def visit_Compare(self, node):
        if any(isinstance(op, ast.In) for op in node.ops):
            for comp in node.comparators:
                if isinstance(comp, ast.Name):
                    if comp.id.lower() in ("memo", "cache", "dp"):
                        self.features["memo_lookup_detected"] = True

        self.generic_visit(node)


# ============================================================
# Public API
# ============================================================

def extract_features(tree: ast.AST) -> dict:
    extractor = FeatureExtractor()
    extractor.visit(tree)

    extractor.features["max_loop_depth"] = extractor.max_loop_depth

    # ---------- BFS ----------
    if (
        extractor.features["while_loops"] >= 1
        and extractor.features["queue_pop_front"]
        and extractor.features["queue_append_detected"]
        and extractor.features["graph_iteration"]
    ):
        extractor.features["bfs_pattern"] = True

    # ---------- Memoization ----------
    if (
        extractor.features["recursion"]
        and extractor.features["memo_dict_defined"]
        and extractor.features["memo_lookup_detected"]
        and extractor.features["memo_store_detected"]
    ):
        extractor.features["memoization_pattern"] = True

    # ---------- Tabulation ----------
    if (
        extractor.features["uses_dp_array"]
        and extractor.features["dp_self_dependency"]
        and extractor.features["for_loops"] >= 1
    ):
        extractor.features["tabulation_pattern"] = True

    # ---------- Final DP ----------
    if (
        extractor.features["memoization_pattern"]
        or extractor.features["tabulation_pattern"]
    ):
        extractor.features["dp_pattern"] = True

    # ---------- Sorting ----------
    if extractor.features["max_loop_depth"] >= 2:
        if extractor.features["adjacent_swap_detected"]:
            extractor.features["bubble_sort_pattern"] = True
            extractor.features["sorting_pattern"] = True

        elif extractor.features["insertion_shift_detected"]:
            extractor.features["insertion_sort_pattern"] = True
            extractor.features["sorting_pattern"] = True

    # ---------- Sliding Window ----------
    if (
        extractor.features["for_loops"] >= 1
        and extractor.features["while_loops"] >= 1
        and extractor.features["window_updates"] >= 1
        and extractor.features["window_shrinks"] >= 1
    ):
        extractor.features["sliding_window_pattern"] = True

    # ---------- Heap ----------
    if (
        extractor.features["heap_imported"]
        and extractor.features["heap_operations"] >= 1
    ):
        extractor.features["heap_pattern"] = True

    return extractor.features