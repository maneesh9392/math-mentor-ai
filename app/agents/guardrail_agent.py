def run_guardrail(problem_text: str):
    """
    Basic safety & sanity checks
    """

    banned_patterns = ["hack", "cheat", "bypass"]

    text_lower = problem_text.lower()

    for word in banned_patterns:
        if word in text_lower:
            return {
                "allowed": False,
                "reason": "Unsafe query detected",
            }

    return {
        "allowed": True,
        "reason": "",
    }