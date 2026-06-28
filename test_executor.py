import os
import pytest
from executor import save_to_file

def test_creates_file():
    filepath = save_to_file("test task", "Test content here.")
    assert os.path.exists(filepath)
    os.remove(filepath)

def test_file_contains_content():
    filepath = save_to_file("test task", "Test content here.")
    with open(filepath, "r") as f:
        content = f.read()
    assert "Test content here." in content
    assert "test task" in content
    os.remove(filepath)