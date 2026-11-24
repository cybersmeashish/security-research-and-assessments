# Development and publication

All development, edits, dependency installation, research analysis, tests and artifact generation must run in OrbStack. Use `docker --context orbstack` explicitly.

Canonical container: `security-research-and-assessments-dev`. Workspace: `/workspaces/security-research-and-assessments/repo`. Persistent volume: `security-research-and-assessments-workspace`. The host copy is for review, transfers and guarded publishing only. Never mount credentials, the home directory or Docker socket. Preserve the named volume. Restore unavailable OrbStack access or report the blocker rather than using host runtimes.

Run relevant checks, update source hashes and distinguish actual observations from synthetic input, design intent, third-party assertions and future work. Preserve account/repository/branch checks, reviewed-file checks, non-forced updates and remote byte verification.
