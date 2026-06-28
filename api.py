from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orchestrator import run
from approval import resolve_approval, get_pending, pending_approvals
from executor import save_to_file
from memory import list_all, load
import os

app = FastAPI()

class TaskRequest(BaseModel):
    task: str

class ApprovalRequest(BaseModel):
    task_id: str
    approved: bool

task_results = {}

@app.post("/task")
def submit_task(req: TaskRequest):
    result = run(req.task, mode="api")
    task_results[result["task_id"]] = {
        "task": req.task,
        "summary": result["summary"]
    }
    return result

@app.post("/approve")
def approve_task(req: ApprovalRequest):
    if req.task_id not in task_results:
        raise HTTPException(status_code=404, detail="Task not found")
    resolve_approval(req.task_id, req.approved)
    if req.approved:
        data = task_results[req.task_id]
        filepath = save_to_file(data["task"], data["summary"])
        return {"status": "saved", "filepath": filepath}
    return {"status": "rejected"}

@app.get("/memory")
def get_memory():
    load()
    memories = list_all()
    return {
        "total": len(memories),
        "memories": [
            {"task": m["task"], "timestamp": m["timestamp"]}
            for m in memories
        ]
    }

@app.get("/history")
def get_history():
    output_dir = "outputs"
    if not os.path.exists(output_dir):
        return {"files": []}
    files = os.listdir(output_dir)
    return {"total": len(files), "files": files}