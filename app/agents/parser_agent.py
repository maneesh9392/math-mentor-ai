import re
from typing import List, Dict
from pydantic import BaseModel


# ===============================
# Output Schema (VERY IMPORTANT)
# ===============================

class ParsedProblem(BaseModel):
    problem_text: str
    topic: str
    variables: List[str]
    constraints: List[str]
    needs_clarification: bool
    ambiguity_reason: str = ""


# ===============================
# Topic Classifier (rule-based)
# ===============================

def classify_topic(text: str) -> str:
    text_lower = text.lower()

    if any(word in text_lower for word in ["probability", "p(", "dice", "coin"]):
        return "probability"

    if any(word in text_lower for word in ["derivative", "differentiate", "limit", "dx"]):
        return "calculus"

    if any(word in text_lower for word in ["matrix", "determinant", "vector"]):
        return "linear_algebra"

    return "algebra"


# ===============================
# Variable Extractor
# ===============================

def extract_variables(text: str) -> List[str]:
    vars_found = re.findall(r"\b[a-zA-Z]\b", text)
    return sorted(list(set(vars_found)))


# ===============================
# Constraint Extractor
# ===============================

def extract_constraints(text: str) -> List[str]:
    patterns = [
        r"[a-zA-Z]\s*[<>]=?\s*\d+",
        r"[a-zA-Z]\s*=\s*\d+",
        r"[a-zA-Z]\s*>\s*0",
        r"[a-zA-Z]\s*<\s*0",
    ]

    constraints = []

    for pattern in patterns:
        matches = re.findall(pattern, text)
        constraints.extend(matches)

    return constraints


# ===============================
# Ambiguity Detector
# ===============================

def detect_ambiguity(text: str) -> tuple[bool, str]:
    text_lower = text.lower()

    # Too short
    if len(text.split()) < 5:
        return True, "Problem statement too short."

    # Missing numbers
    if not re.search(r"\d", text):
        return True, "No numeric values detected."

    # Contains OCR noise patterns
    noise_patterns = ["??", "…", "___"]
    if any(p in text for p in noise_patterns):
        return True, "Possible OCR corruption detected."

    return False, ""


# ===============================
# Text Cleaner
# ===============================

def clean_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


# ===============================
# MAIN PARSER AGENT
# ===============================

def run_parser_agent(raw_text: str) -> Dict:
    """
    Main entry point for Parser Agent
    """

    cleaned = clean_text(raw_text)

    topic = classify_topic(cleaned)
    variables = extract_variables(cleaned)
    constraints = extract_constraints(cleaned)

    needs_clarification, reason = detect_ambiguity(cleaned)

    parsed = ParsedProblem(
        problem_text=cleaned,
        topic=topic,
        variables=variables,
        constraints=constraints,
        needs_clarification=needs_clarification,
        ambiguity_reason=reason,
    )

    return parsed.dict()