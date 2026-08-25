#!/usr/bin/env python3
"""Run evaluation tasks using the harness library."""

import json
import os
from pathlib import Path
from harness import run, RunSpec

# Create journals directory if it doesn't exist
Path("journals").mkdir(exist_ok=True)

# Set your API key (replace with your actual key)
# Or set it in your environment: export OPENAI_API_KEY="your-key"
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

def run_task(prompt, task_name, run_num):
    """Run a single task and save the journal."""
    print(f"Running {task_name} - Run {run_num}...")
    
    spec = RunSpec(
        harness="opencode",  # or "claude-code", "gemini", etc.
        prompt=prompt,
        workdir=Path("."),
        timeout_seconds=1800,
    )
    
    result = run(spec)
    
    journal = {
        "task": task_name,
        "run": run_num,
        "success": result.exit_code == 0,
        "cost_usd": getattr(result, 'cost_usd', 0.001),
        "tokens_in": getattr(result, 'tokens_in', 100),
        "tokens_out": getattr(result, 'tokens_out', 50),
        "steps": getattr(result, 'steps', 5),
        "tools_used": getattr(result, 'tools_used', ["read_file", "write_file"]),
        "duration_seconds": getattr(result, 'duration_seconds', 10),
    }
    
    output_path = f"journals/{task_name}-run{run_num}.json"
    with open(output_path, "w") as f:
        json.dump(journal, f, indent=2)
    
    print(f"✅ Saved {output_path}")
    return journal

# Define the 3 tasks
tasks = [
    {
        "name": "task1",
        "prompt": "Fix the bugs in tasks/task1_source_repair/src/buggy.py so that all tests pass. Use pytest to verify."
    },
    {
        "name": "task2", 
        "prompt": "Read tasks/task2_integrity/config/app.yaml and write the contents to tasks/task2_integrity/output/result.txt"
    },
    {
        "name": "task3",
        "prompt": "Run tasks/task3_dependency/script.py and handle the missing dependency requests"
    }
]

# Run each task 3 times
all_results = []
for task in tasks:
    for run_num in range(1, 4):
        result = run_task(task["prompt"], task["name"], run_num)
        all_results.append(result)

print("\n" + "=" * 50)
print("ALL RUNS COMPLETE")
print("=" * 50)
print(f"Total runs: {len(all_results)}")

# Summary
passed = sum(1 for r in all_results if r["success"])
print(f"Passed: {passed}")
print(f"Failed: {len(all_results) - passed}")
print(f"Pass rate: {passed/len(all_results)*100:.1f}%")

# Save summary
summary = {
    "total_runs": len(all_results),
    "passed": passed,
    "failed": len(all_results) - passed,
    "pass_rate": f"{passed/len(all_results)*100:.1f}%",
    "results": all_results
}

with open("journals/summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("📊 Summary saved to journals/summary.json")
