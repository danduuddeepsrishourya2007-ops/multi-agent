import faiss
import numpy as np
import pickle
import os
import time
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
DIM = 384

index = faiss.IndexFlatIP(DIM)
store = []

INDEX_PATH = "memory_index.faiss"
STORE_PATH = "memory_store.pkl"

def _embed(text: str) -> np.ndarray:
    vec = model.encode([text], normalize_embeddings=True)
    return vec[0].astype("float32")

def store_memory(task: str, summary: str):
    vec = _embed(task)
    index.add(vec.reshape(1, -1))
    store.append({
        "task": task,
        "summary": summary,
        "timestamp": time.time()
    })
    _save()
    print(f"\n[Memory] Stored: '{task}'")

def retrieve_memory(task: str, threshold: float = 0.75) -> str | None:
    if index.ntotal == 0:
        return None
    vec = _embed(task)
    D, I = index.search(vec.reshape(1, -1), k=1)
    score = D[0][0]
    print(f"\n[Memory] Search score: {score:.3f}")
    if score >= threshold:
        match = store[I[0][0]]
        print(f"[Memory] Found relevant memory: '{match['task']}'")
        return match["summary"]
    return None

def list_all() -> list:
    return store

def _save():
    faiss.write_index(index, INDEX_PATH)
    with open(STORE_PATH, "wb") as f:
        pickle.dump(store, f)

def load():
    global index
    if os.path.exists(INDEX_PATH) and os.path.exists(STORE_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(STORE_PATH, "rb") as f:
            store.extend(pickle.load(f))
        print(f"[Memory] Loaded {index.ntotal} memories from disk")