# Mahu Test Subskill

Use for tests, QA plans, smoke tests, regression checks, acceptance criteria,
and evidence collection.

Owner: `testboat`.

## Prerequisites

Required CLI: `testboat`

Check before execution:

```bash
testboat --help
# or
mahu doctor --subskill test
```

Install if missing:

```bash
pip install testboat
```

If `testboat` is missing and you do not have permission to install packages,
stop and ask the user. You may still run the repository's native tests if the
user asks for a direct test pass, but do not claim testboat coverage.

## SOP

1. Clarify the risk surface and acceptance criteria.
2. Identify deterministic checks before exploratory checks.
3. Run the smallest useful test first.
4. Add regression tests for bugs that were just fixed.
5. Capture test evidence: command, result, and remaining risk.
6. Route product/UI defects to fdesign, deck defects to fppt, and review-loop defects to floop-client.

## Guardrails

- Do not call work done without running the relevant checks.
- Do not claim coverage or pass status without command evidence.
- Prefer repeatable tests over visual inspection alone.
