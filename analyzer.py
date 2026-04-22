import ast

from features import extract_features
from rules import detect_algorithm
from complexity import estimate_complexity
from explanations import generate_explanation


# -----------------------------
# Local parser (removes dependency)
# -----------------------------
def parse_code(source: str):
    return ast.parse(source)


# -----------------------------
# Main analysis function
# -----------------------------
def analyze_code(source: str) -> dict:
    """
    Pure rule-based analysis pipeline.

    Steps:
    1. Parse source code into AST
    2. Extract structural features
    3. Detect algorithm pattern
    4. Estimate time complexity
    5. Generate explanation
    """

    # Step 1: Parse
    tree = parse_code(source)

    # Step 2: Feature extraction
    features = extract_features(tree)

    # Step 3: Rule-based detection
    detection = detect_algorithm(features)

    # Step 4: Complexity estimation
    complexity = estimate_complexity(features)

    # Normalize set → list (for JSON / Jupyter display)
    if "function_calls" in features:
        features["function_calls"] = list(features["function_calls"])

    # Step 5: Explanation generation
    base_result = {
        "features": features,
        "analysis": detection,
        "complexity": complexity,
    }

    explanation = generate_explanation(base_result)

    # Final output
    return {
        "pattern": detection.get("pattern"),
        "category": detection.get("category"),
        "time_complexity": complexity.get("time_complexity"),
        "summary": explanation.get("summary"),
    }