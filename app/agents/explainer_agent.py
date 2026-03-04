def run_explainer_agent(parsed_problem: dict, solver_output: dict):
    """
    Generates student-friendly explanation
    """

    problem = parsed_problem["problem_text"]
    result = solver_output["result"]

    explanation = f"""
Step-by-step solution:

1. We interpret the problem as:
   {problem}

2. We apply the appropriate mathematical method.

3. Solving gives the result:
   {result}

4. Therefore, the final answer is:
   {result}
"""

    return explanation.strip()