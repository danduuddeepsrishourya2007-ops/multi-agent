import pytest
import faiss
from memory import store_memory, retrieve_memory, index, store

def setup_function():
    index.reset()
    store.clear()

def test_store_and_retrieve():
    store_memory("what is Bitcoin", "Bitcoin is a cryptocurrency.")
    result = retrieve_memory("what is Bitcoin")
    assert result == "Bitcoin is a cryptocurrency."

def test_similar_query_retrieves():
    store_memory("what is Bitcoin", "Bitcoin is a cryptocurrency.")
    result = retrieve_memory("explain Bitcoin to me")
    assert result is not None

def test_unrelated_query_returns_none():
    store_memory("what is Bitcoin", "Bitcoin is a cryptocurrency.")
    result = retrieve_memory("what is the capital of Japan")
    assert result is None

def test_empty_memory_returns_none():
    result = retrieve_memory("anything")
    assert result is None