# Structured GenAI and University Learning

**Author:** David Yakubov | Research Methods | Task 2

## Overview and research question

Does structured generative-AI-assisted learning, compared with traditional independent learning, improve university students' academic performance, reduce task-completion time, and improve critical thinking?

This repository continues the author's Task 1 proposal submitted on 27 September 2026. It provides a measurement and descriptive-analysis pipeline for the planned human-participant experiment. It does not benchmark LLM response speed. No participants have been recruited and no real experimental results are claimed here.

The treatment protocol requires students to verify, critique and improve AI answers. The control group uses the same course materials without generative AI. Both groups take the final assessments without AI.

## System requirements

- CPython **3.12.14**, standard library only; no third-party Python dependencies.
- Windows, Linux or macOS; Docker is optional.
- UTF-8 CSV input with the schema below.

## Quickstart guide

After downloading/extracting this repository, open a terminal inside it:

```sh
python --version
python src/benchmark.py --config configs/config.json
```

Use Python 3.12.14 for the reference environment. The sample run writes `results/sample_summary.json` and `results/sample_run.log`. These files contain **synthetic smoke-test results, not research evidence**. Relative paths in the configuration resolve against the repository root, independent of the terminal's working directory. No API keys, paid AI services or network requests are needed to run the pipeline.

Optional container run (requires Docker):

```sh
docker build -t genai-learning-study .
docker run --rm genai-learning-study
```

The container prints its summary to standard output. To retain files on the host, mount a writable host directory at `/app/results`. The base image fixes the Python patch version; the Docker image itself is not digest-pinned and can change between builds. The native Python pipeline has been tested; Docker verification status is recorded in `docs/validation.md`.

## Planned benchmarks / comparisons

| Question | Comparison | Metric | Role |
|---|---|---|---|
| Academic performance | Structured GenAI vs traditional | Post-test minus pre-test, percentage points (0-100 scales) | Primary, baseline-adjusted refinement of Task 1 |
| Learning efficiency | Structured GenAI vs traditional | Task time in minutes, lower is better | Secondary |
| Critical thinking | Structured GenAI vs traditional | Blinded rubric score, 0-20 | Secondary and guardrail |
| Task 1 continuity | Structured GenAI vs traditional | Raw post-test score, 0-100 | Descriptive supporting metric |

The program validates rows, calculates group means and treatment-minus-control differences, and checks configured descriptive guardrails. It deliberately does not calculate statistical significance or claim that hypotheses are confirmed. See the prospective analysis plan and restrictions in `docs/methodology.md`.

## Data schema

`participant_id,group,pretest_score,posttest_score,task_minutes,critical_thinking_score`

- One row per participant; pseudonymous unique identifier only.
- `group`: `traditional` or `genai`.
- Pre/post tests: 0-100; critical thinking: 0-20; time: >0 and <=40 minutes.
- Missing, duplicate, invalid or non-finite values fail validation. Both groups are required.
- `/data/sample/participants.csv` contains **10 invented rows for software testing**.
- Keep real participant data outside the public repository. Do not commit names, emails, consent records, private prompts or participant answers.

## Structure

```text
configs/config.json       Experiment settings and measurement limits
data/sample/participants.csv  Synthetic input, 10 rows
src/benchmark.py           Validated descriptive-analysis runner
tests/test_benchmark.py    Checks calculations and malformed inputs
docs/methodology.md        Methodology passport and prospective protocol
docs/validation.md         Local verification record
Dockerfile                Python 3.12.14 execution environment
requirements.txt          No third-party dependencies
LICENSE                   MIT
```

## Validation

```sh
python -m unittest discover -s tests -v
```

## Citation / License

Yakubov, David (2026). *Structured GenAI and University Learning*. Research Methods, Task 2. Based on the author's Task 1 proposal, *The Impact of Generative AI on University Students' Learning Performance and Critical Thinking*.

Code and synthetic sample data: MIT License, see `LICENSE`. Do not publish participant data under this license; the repository contains no real participant dataset.
