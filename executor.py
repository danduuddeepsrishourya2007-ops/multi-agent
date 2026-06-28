import os
import time

OUTPUT_DIR = "outputs"

def save_to_file(task: str, content: str) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = task[:30].strip().replace(" ", "_") + f"_{int(time.time())}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w") as f:
        f.write(f"Task: {task}\n\n")
        f.write(content)
    print(f"\n[Executor] Saved to {filepath}")
    return filepath