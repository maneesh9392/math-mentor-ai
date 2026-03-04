import sympy as sp
import re


# ===============================
# Preprocess math text
# ===============================
def extract_equation(text: str) -> str:
    """
    Extracts the main equation from natural language text.
    Example:
    'Solve for x: 2x + 5 = 15' -> '2x + 5 = 15'
    """

    # If colon exists, take RHS (common pattern)
    if ":" in text:
        text = text.split(":", 1)[1]

    # Remove common instruction words
    text = text.lower()
    noise_phrases = [
        "solve for x",
        "solve",
        "find x",
        "find the value of x",
        "calculate",
    ]

    for phrase in noise_phrases:
        text = text.replace(phrase, "")

    return text.strip()

def normalize_expression(expr: str) -> str:
    expr = expr.replace(" ", "")

    # number followed by variable: 2x -> 2*x
    expr = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", expr)

    # number followed by (: 2(x+1) -> 2*(x+1)
    expr = re.sub(r"(\d)\(", r"\1*(", expr)

    return expr

# ===============================
# Algebra Solver
# ===============================

def solve_algebra(problem_text: str):
    try:
        # ✅ NEW — extract equation first
        equation_text = extract_equation(problem_text)

        # ✅ normalize math
        clean = normalize_expression(equation_text)

        # find equation
        match = re.search(r"(.+?)=(.+)", clean)
        if not match:
            return None, f"Could not parse equation from: {clean}"

        left, right = match.groups()

        x = sp.symbols("x")

        equation = sp.Eq(sp.sympify(left), sp.sympify(right))
        solution = sp.solve(equation, x)

        return solution, ""

    except Exception as e:
        return None, str(e)


# ===============================
# Calculus Solver
# ===============================

def solve_calculus(problem_text: str):
    try:
        x = sp.symbols("x")

        text = problem_text.replace(" ", "")

        # detect x^n
        match = re.search(r"x\^(\d+)", text)
        if match:
            power = int(match.group(1))
            expr = x ** power
            derivative = sp.diff(expr, x)
            return derivative, ""

        return None, "Could not parse derivative."

    except Exception as e:
        return None, str(e)


# ===============================
# MAIN SOLVER AGENT
# ===============================

def run_solver_agent(parsed_problem: dict, route: str):
    text = parsed_problem["problem_text"]

    if route == "calculus_solver":
        result, err = solve_calculus(text)
    else:
        result, err = solve_algebra(text)

    return {
        "result": str(result),
        "error": err,
        "confidence": 0.9 if result else 0.4,
    }