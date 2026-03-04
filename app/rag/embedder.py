from sentence_transformers import SentenceTransformer
import numpy as np

# load once (important)
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts):
    """
    Returns numpy embeddings
    """
    return model.encode(texts, convert_to_numpy=True)


def embed_query(text):
    return model.encode([text], convert_to_numpy=True)[0]