---
name: Use py launcher for Python scripts
description: On this Windows system, use `py` command (not `python` or `python3`) to run Python scripts
type: feedback
---

Use the `py` launcher to run Python scripts on this Windows system.

**Why:** The Microsoft Store aliases for `python`/`python3` are enabled but don't point to a real installation, causing "Python was not found" errors. The `py` launcher is the standard Windows Python launcher that correctly finds installed Python versions.

**How to apply:** When running Python scripts in this project, use `py script.py` instead of `python script.py` or `python3 script.py`.
