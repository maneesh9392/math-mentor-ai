import os
import faiss
import pickle
from app.rag.embedder import embed_texts

KB_PATH = "data/knowledge_base"
INDEX_PATH = "data/vector_store"
os.makedirs(INDEX_PATH, exist_ok=True)


def chunk_text(text, chunk_size=300, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def load_documents():
    docs = []

    for file in os.listdir(KB_PATH):
        if file.endswith(".txt"):
            with open(os.path.join(KB_PATH, file), "r", encoding="utf-8") as f:
                docs.append((file, f.read()))

    return docs


def build_vector_store():
    docs = load_documents()

    all_chunks = []
    metadata = []

    for filename, text in docs:
        chunks = chunk_text(text)

        for chunk in chunks:
            all_chunks.append(chunk)
            metadata.append({"source": filename, "text": chunk})

    embeddings = embed_texts(all_chunks)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # save
    faiss.write_index(index, f"{INDEX_PATH}/faiss.index")

    with open(f"{INDEX_PATH}/metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print("✅ Vector store built!")


if __name__ == "__main__":
    build_vector_store()