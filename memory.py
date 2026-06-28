import faiss
import numpy as np
import time
import os
import json
from sentence_transformers import SentenceTransformer
from supabase import create_client

model = SentenceTransformer("all-MiniLM-L6-v2")
DIM = 384

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

index = faiss.IndexFlatIP(DIM)
store = []

def _embed(text: str) -> np.ndarray:
    vec = model.encode([text], normalize_embeddings=True)
    return vec[0].astype("float32")

def store_memory(task: str, summary: str):
    vec = _embed(task)
    index.add(vec.reshape(1, -1))
    store.append({"task": task, "summary": summary, "timestamp": time.time()})
    supabase.table("memories").insert({
        "task": task,
        "summary": summary,
        "embedding": json.dumps(vec.tolist()),
        "timestamp": time.time()
    }).execute()
    print(f"[Memory] Stored: '{task}'")

def retrieve_memory(task: str, threshold: float = 0.75) -> str | None:
    if index.ntotal == 0:
        return None
    vec = _embed(task)
    D, I = index.search(vec.reshape(1, -1), k=1)
    score = D[0][0]
    print(f"[Memory] Search score: {score:.3f}")
    if score >= threshold:
        match = store[I[0][0]]
        print(f"[Memory] Found: '{match['task']}'")
        return match["summary"]
    return None

def list_all() -> list:
    return store

def load():
    global index
    res = supabase.table("memories").select("*").execute()
    rows = res.data
    if not rows:
        print("[Memory] No memories in Supabase")
        return
    for row in rows:
        vec = np.array(json.loads(row["embedding"]), dtype="float32")
        index.add(vec.reshape(1, -1))
        store.append({"task": row["task"], "summary": row["summary"], "timestamp": row["timestamp"]})
    print(f"[Memory] Loaded {len(rows)} memories from Supabase")