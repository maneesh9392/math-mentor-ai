def run_verifier_agent(parsed_problem: dict, solver_output: dict):
    """
    Checks solver confidence and errors
    """

    if solver_output["error"]:
        return {
            "verified": False,
            "reason": solver_output["error"],
            "confidence": 0.4,
        }

    if solver_output["confidence"] < 0.6:
        return {
            "verified": False,
            "reason": "Low solver confidence",
            "confidence": solver_output["confidence"],
        }

    return {
        "verified": True,
        "reason": "",
        "confidence": solver_output["confidence"],
    }