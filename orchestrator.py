from agents import researcher_agent, writer_agent
from memory import retrieve_memory, store_memory, load
from approval import terminal_approval, request_approval
from executor import save_to_file
import uuid

def run(task: str, mode: str = "terminal") -> dict:
    load()

    print(f"\n[Orchestrator] Task received: {task}")

    past_context = retrieve_memory(task)
    if past_context:
        print("[Orchestrator] Using memory context")
    else:
        print("[Orchestrator] No relevant memory found")

    research = researcher_agent(task, past_context)
    summary = writer_agent(research, task)

    store_memory(task, summary)

    if mode == "terminal":
        approved = terminal_approval("Save summary to file", summary)
        if approved:
            filepath = save_to_file(task, summary)
            return {"status": "saved", "filepath": filepath, "summary": summary}
        return {"status": "rejected", "summary": summary}

    elif mode == "api":
        task_id = str(uuid.uuid4())[:8]
        request_approval(task_id, "Save summary to file", summary)
        return {
            "task_id": task_id,
            "status": "pending_approval",
            "summary": summary
        }