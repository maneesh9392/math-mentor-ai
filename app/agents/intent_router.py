def route_intent(parsed_problem: dict) -> str:
    """
    Routes problem to appropriate solver strategy
    """
    topic = parsed_problem.get("topic", "algebra")

    if topic == "calculus":
        return "calculus_solver"
    elif topic == "probability":
        return "probability_solver"
    elif topic == "linear_algebra":
        return "linear_solver"
    else:
        return "algebra_solver"