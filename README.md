# Multi-Agent System with Memory & Human Approval Flows

A production AI system where specialized agents collaborate to research, write, and save outputs — with human approval before any action is taken.

## Live Demo
https://multi-agent-production-3990.up.railway.app/docs

## How it works
1. User submits a task via POST /task
2. Researcher agent searches the web using DuckDuckGo
3. Writer agent drafts a summary from the research
4. System pauses — waits for human approval
5. On approval → Executor saves output to file
6. Memory stores every completed task for future context

## Stack
- FastAPI
- Groq (LLaMA 3.1 8b)
- DuckDuckGo Search
- FAISS + sentence-transformers (long-term memory)
- Railway (deployment)

## Agents
- Researcher — web search + fact extraction
- Writer — structured summary from research
- Executor — saves approved output to disk

## Results
- 14/14 pytest cases passing
- Memory retrieval working across sessions
- Human approval gate tested with approve and reject flows

## Endpoints
- POST /task — submit a research task
- POST /approve — approve or reject pending action
- GET /memory — view stored memories
- GET /history — view saved output files

## Run locally
pip install -r requirements.txt
uvicorn api:app --reload