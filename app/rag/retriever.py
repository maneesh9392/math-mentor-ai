import faiss
import pickle
import numpy as np
import os

from app.rag.embedder import embed_query
from app.rag.ingest import build_vector_store

INDEX_PATH = "data/vector_store/faiss.index"
META_PATH = "data/vector_store/metadata.pkl"


# ✅ If vector DB doesn't exist → build it
if not os.path.exists(INDEX_PATH):
    print("Vector store missing — building...")
    build_vector_store()

# Load index
index = faiss.read_index(INDEX_PATH)

with open(META_PATH, "rb") as f:
    metadata = pickle.load(f)


def retrieve_context(query, top_k=3):
    query_vec = embed_query(query).astype("float32")
    query_vec = np.expand_dims(query_vec, axis=0)

    distances, indices = index.search(query_vec, top_k)

    results = []
    for idx in indices[0]:
        results.append(metadata[idx])

    return results