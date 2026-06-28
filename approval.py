pending_approvals = {}

def request_approval(task_id: str, action: str, preview: str):
    pending_approvals[task_id] = {
        "action": action,
        "preview": preview,
        "approved": None
    }
    print(f"\n[Approval] Pending approval for task: {task_id}")

def resolve_approval(task_id: str, approved: bool) -> bool:
    if task_id not in pending_approvals:
        return False
    pending_approvals[task_id]["approved"] = approved
    return True

def get_pending() -> dict:
    return {k: v for k, v in pending_approvals.items() if v["approved"] is None}

def terminal_approval(action: str, preview: str) -> bool:
    print("\n" + "="*50)
    print("[Human Approval Required]")
    print(f"Action: {action}")
    print(f"\nPreview:\n{preview[:500]}...")
    print("="*50)
    response = input("\nApprove? (y/n): ").strip().lower()
    if response == "y":
        print("[Approved] Proceeding...")
        return True
    print("[Rejected] Action cancelled.")
    return False