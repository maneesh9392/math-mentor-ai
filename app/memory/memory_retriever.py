import os
import json
import numpy as np
from app.rag.embedder import embed_query

MEMORY_DIR = "data/memory_store"


def load_all_memories():
    memories = []

    if not os.path.exists(MEMORY_DIR):
        return memories

    for file in os.listdir(MEMORY_DIR):
        if file.endswith(".json"):
            with open(os.path.join(MEMORY_DIR, file), "r", encoding="utf-8") as f:
                memories.append(json.load(f))

    return memories


def retrieve_similar_problem(query_text, top_k=1):
    memories = load_all_memories()

    if not memories:
        return None

    query_vec = embed_query(query_text)

    best_score = -1
    best_memory = None

    for mem in memories:
        past_text = mem["parsed_problem"]["problem_text"]
        past_vec = embed_query(past_text)

        score = np.dot(query_vec, past_vec)

        if score > best_score:
            best_score = score
            best_memory = mem

    if best_score > 0.85:  # similarity threshold
        return best_memory

    return None