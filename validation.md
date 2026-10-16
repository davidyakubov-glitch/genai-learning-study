# Validation record

Date: 17 October 2026. Platform: Windows. Interpreter: CPython 3.12.14.

- Sample pipeline: passed; 10 synthetic rows, 5 records per arm; JSON and log generated.
- Four automated tests: passed. They check hand-calculated means/differences, invalid or non-finite values, duplicate IDs, missing groups, critical-thinking decline and the time cap.
- Runner also executed successfully from outside the repository directory.
- Smoke-test gain means: control 10.2, treatment 16.0 percentage points; difference 5.8. Task-time difference: -5.4 minutes. These are expected values from invented fixtures, not study findings.
- Docker was not installed in the local validation environment. The Dockerfile is supplied but its build/run has not been verified here. The directly tested Python route requires no third-party dependencies.
- Real-participant collection, model access, assessment administration and statistical inference are not covered by these software tests.
