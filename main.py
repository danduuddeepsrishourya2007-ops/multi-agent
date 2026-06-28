from orchestrator import run

if __name__ == "__main__":
    task = input("Enter task: ")
    result = run(task, mode="terminal")
    print(f"\n[Final Output]\n{result['summary']}")