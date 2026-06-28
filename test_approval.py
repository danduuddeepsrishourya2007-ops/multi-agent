from approval import terminal_approval, request_approval, resolve_approval, get_pending, pending_approvals
from unittest.mock import patch

def setup_function():
    pending_approvals.clear()

def test_terminal_approval_yes():
    with patch("builtins.input", return_value="y"):
        result = terminal_approval("Save file", "Preview text")
        assert result == True

def test_terminal_approval_no():
    with patch("builtins.input", return_value="n"):
        result = terminal_approval("Save file", "Preview text")
        assert result == False

def test_request_approval_creates_pending():
    request_approval("abc123", "Save file", "Preview")
    assert "abc123" in pending_approvals
    assert pending_approvals["abc123"]["approved"] is None

def test_resolve_approval_true():
    request_approval("abc123", "Save file", "Preview")
    resolve_approval("abc123", True)
    assert pending_approvals["abc123"]["approved"] == True

def test_resolve_approval_false():
    request_approval("abc123", "Save file", "Preview")
    resolve_approval("abc123", False)
    assert pending_approvals["abc123"]["approved"] == False