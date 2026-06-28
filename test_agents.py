import pytest
from unittest.mock import patch
from agents import researcher_agent, writer_agent

def test_researcher_returns_string():
    with patch("agents.web_search", return_value="Bitcoin is a cryptocurrency."):
        with patch("agents.call_llm", return_value="Key facts about Bitcoin."):
            result = researcher_agent("research Bitcoin")
            assert isinstance(result, str)
            assert len(result) > 0

def test_researcher_uses_past_context():
    with patch("agents.web_search", return_value="New info."):
        with patch("agents.call_llm", return_value="Updated facts.") as mock_llm:
            researcher_agent("research Bitcoin", past_context="Old Bitcoin info")
            prompt_used = mock_llm.call_args[0][0]
            assert "Old Bitcoin info" in prompt_used

def test_writer_returns_string():
    with patch("agents.call_llm", return_value="A well written summary."):
        result = writer_agent("Some research facts.", "research Bitcoin")
        assert isinstance(result, str)
        assert len(result) > 0