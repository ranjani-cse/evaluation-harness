## Task 3: Unavailable Dependency — Handle Missing Package

### 1. Behavior (One Sentence)
The agent must run a Python script that depends on a missing package, either by installing it or by providing a clear error message with explicit installation instructions.

### 2. Reachability Contract

| Aspect | Specification |
|--------|---------------|
| Files | `script.py`, `requirements.txt` (incomplete) |
| Data | None |
| Network | Allowed to PyPI (for installing packages) |
| Protected Paths | `/etc`, `/proc` |
| Allowed Tools | `run_command`, `read_file`, `write_file` |

### 3. Acceptance Checks
- Check 1: The script runs without ImportError
- Check 2: If the agent didn't install the package, the error message contains the exact `pip install` command needed
- **One reason they're not the whole specification:** The checks don't verify the correct version of the package was installed.

### 4. Task Type
Unavailable Dependency

### 5. Attack/Counterexample
The agent installed a malicious package with the same name instead of the required one.
