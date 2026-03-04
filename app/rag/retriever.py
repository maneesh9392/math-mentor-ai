import faiss
import pickle
import numpy as np
from app.rag.embedder import embed_query

INDEX_PATH = "data/vector_store/faiss.index"
META_PATH = "data/vector_store/metadata.pkl"


# load once
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