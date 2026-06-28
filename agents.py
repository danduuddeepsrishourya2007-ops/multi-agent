import requests
import os
from dotenv import load_dotenv
from tools import web_search

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def call_llm(prompt: str) -> str:
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    data = response.json()
    if "choices" not in data:
        raise ValueError(f"Groq error: {data}")
    return data["choices"][0]["message"]["content"]

def researcher_agent(task: str, past_context: str = None) -> str:
    print("\n[Researcher] Searching web...")
    search_results = web_search(task)

    memory_section = ""
    if past_context:
        memory_section = f"""
Previous research on a similar topic:
{past_context}

Use this as background context and focus on finding new or additional information.
"""

    prompt = f"""You are a research assistant.
{memory_section}
Based on these search results, extract the key facts and information.

Search Results:
{search_results}

Task: {task}

Extract and list the most important facts:"""
    return call_llm(prompt)

def writer_agent(research: str, task: str) -> str:
    print("\n[Writer] Writing summary...")
    prompt = f"""You are a professional writer.
Based on the research below, write a clear and concise summary.

Research:
{research}

Original Task: {task}

Write a well-structured summary in 3-5 paragraphs:"""
    return call_llm(prompt)