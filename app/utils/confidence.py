def needs_hitl(confidence, threshold=0.75):
    """
    Decide whether Human-in-the-Loop is required
    """
    return confidence < threshold