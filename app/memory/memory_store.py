import os
import json
import uuid
from datetime import datetime

MEMORY_DIR = "data/memory_store"
os.makedirs(MEMORY_DIR, exist_ok=True)


def store_interaction(
    raw_input,
    parsed_problem,
    retrieved_context,
    solver_output,
    verifier_output,
    user_feedback=None,
):
    """
    Stores one full interaction for self-learning
    """

    record = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "raw_input": raw_input,
        "parsed_problem": parsed_problem,
        "retrieved_context": retrieved_context,
        "solver_output": solver_output,
        "verifier_output": verifier_output,
        "user_feedback": user_feedback,
    }

    path = os.path.join(MEMORY_DIR, f"{record['id']}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)

    return record["id"]