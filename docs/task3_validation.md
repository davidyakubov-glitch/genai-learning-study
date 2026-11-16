# Task 3 verification record

Verified locally on 16 November 2026 with CPython 3.12.14 on Windows.

- Original Task 2 unit suite: 4 tests passed.
- Task 3 group means and differences match the original Task 2 runner exactly for the unchanged fixture.
- Invalid-input probes: duplicate ID, missing field, time above cap, NaN, real-data marker, and warm-up phase each raised a validation error as intended.
- Notebook executed from the `notebooks/` directory using a fresh Python kernel. All five code cells completed sequentially (1–5), with saved output and no error outputs. Both plot images are embedded.
- Both PNG figures: 2400 × 1620 pixels at 300 DPI. Labels, captions, units and SD bars visually inspected. Both vector PDF versions exported from the same Matplotlib figures.
- No real observations, API calls, participant adherence verification, inferential tests or LLM training are represented by these checks.

Direct dependency versions are recorded in `requirements-task3.txt`. This is not a complete platform-independent dependency lock. The preserved original Dockerfile is for Task 2 only; Task 3 was tested natively, not in Docker.

The source snapshot is identified in README. The owner authorized publication of the Task 3 update. A final GitHub release remains a separate submission step. Keep real participant information outside the public repository.
