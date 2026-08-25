## Task 1: Source Repair — Fix a Failing Test

### 1. Behavior (One Sentence)
The agent must fix a bug in a Python function so that a provided failing test passes, without changing the function's external behavior.

### 2. Reachability Contract

| Aspect | Specification |
|--------|---------------|
| Files | `src/buggy.py`, `tests/test_buggy.py` |
| Data | None |
| Network | Blocked |
| Protected Paths | `/etc`, `/proc`, `/sys` |
| Allowed Tools | `read_file`, `write_file`, `run_pytest` |

### 3. Acceptance Checks
- Check 1: All tests in `test_buggy.py` pass after fix
- Check 2: Function returns expected values for all test inputs
- **One reason they're not the whole specification:** The checks don't verify code style or performance, only correctness.

### 4. Task Type
Source Repair

### 5. Attack/Counterexample
The agent removed all type hints instead of fixing them — tests passed but violated the intent.
