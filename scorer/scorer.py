import json
import os
from pathlib import Path

def score_run(journal_path):
    """Score a single run from its JSON journal."""
    with open(journal_path, 'r') as f:
        data = json.load(f)
    
    return {
        "pass_fail": data.get("success", False),
        "steps_taken": data.get("steps", 0),
        "tools_used": data.get("tools_used", []),
        "cost": data.get("cost_usd", 0.0)
    }

def score_all_journals(journals_dir):
    """Score all JSON journals in a directory."""
    results = {}
    for file in os.listdir(journals_dir):
        if file.endswith('.json'):
            path = os.path.join(journals_dir, file)
            results[file] = score_run(path)
    return results

def rescore_with_threshold(journals_dir, max_steps=6):
    """Rescore with a different threshold (no model call)."""
    results = {}
    for file in os.listdir(journals_dir):
        if file.endswith('.json'):
            path = os.path.join(journals_dir, file)
            with open(path, 'r') as f:
                data = json.load(f)
            results[file] = {
                "pass_fail": data.get("steps", 0) <= max_steps,
                "steps_taken": data.get("steps", 0),
                "tools_used": data.get("tools_used", []),
                "cost": data.get("cost_usd", 0.0)
            }
    return results

if __name__ == "__main__":
    # Go up one directory to find journals
    journals_dir = "../journals"
    
    # Check if journals directory exists
    if not os.path.exists(journals_dir):
        print(f"❌ Journals directory not found: {journals_dir}")
        print("Creating mock journals for demonstration...")
        os.makedirs(journals_dir, exist_ok=True)
        # Create mock journals
        mock_data = [
            ("task1-run1", True, 5, ["read_file", "write_file", "run_pytest"], 0.002),
            ("task1-run2", True, 7, ["read_file", "write_file", "run_pytest"], 0.003),
            ("task1-run3", False, 10, ["read_file", "write_file"], 0.004),
            ("task2-run1", True, 4, ["read_file", "write_file"], 0.001),
            ("task2-run2", False, 8, ["read_file"], 0.003),
            ("task2-run3", True, 6, ["read_file", "write_file"], 0.002),
            ("task3-run1", True, 8, ["run_command", "read_file"], 0.004),
            ("task3-run2", True, 6, ["run_command", "read_file", "write_file"], 0.003),
            ("task3-run3", False, 12, ["run_command"], 0.005),
        ]
        for name, success, steps, tools, cost in mock_data:
            journal = {
                "task": name.split("-")[0],
                "run": int(name.split("-")[1].replace("run", "")),
                "success": success,
                "steps": steps,
                "tools_used": tools,
                "cost_usd": cost
            }
            with open(f"{journals_dir}/{name}.json", "w") as f:
                json.dump(journal, f, indent=2)
        print(f"✅ Created {len(mock_data)} mock journals in {journals_dir}/")
    
    print("=" * 50)
    print("INITIAL SCORING")
    print("=" * 50)
    
    results = score_all_journals(journals_dir)
    
    for run, score in results.items():
        pass_fail = "✅ PASS" if score["pass_fail"] else "❌ FAIL"
        tools_count = len(score["tools_used"])
        print(f"{run}: {pass_fail} | Steps: {score['steps_taken']} | Tools: {tools_count} | Cost: ${score['cost']:.4f}")
    
    total = len(results)
    passed = sum(1 for r in results.values() if r["pass_fail"])
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total runs: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Pass rate: {passed/total*100:.1f}%")
    print(f"Total cost: ${sum(r['cost'] for r in results.values()):.4f}")
    
    # Show scoring change
    print("\n" + "=" * 50)
    print("SCORING CHANGE (Rescore without model call)")
    print("=" * 50)
    print("Changing pass/fail threshold: Steps <= 6 now passes")
    
    rescored = rescore_with_threshold(journals_dir, max_steps=6)
    
    for run, score in rescored.items():
        pass_fail = "✅ PASS" if score["pass_fail"] else "❌ FAIL"
        print(f"{run}: {pass_fail} | Steps: {score['steps_taken']}")
    
    rescored_passed = sum(1 for r in rescored.values() if r["pass_fail"])
    print(f"\nAfter rescore: {rescored_passed} passes out of {total}")
    print(f"Change: {rescored_passed - passed} run(s) changed status")
